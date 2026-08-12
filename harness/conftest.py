"""Harness fixtures and the pytest plugin that turns results into a scorecard.

The harness is black-box: it talks HTTP to whatever ``--base-url`` points at
and knows nothing about how that thing is built. Everything it needs, it either
creates through the public API or skips with a reason.
"""

from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from report import Scorecard  # noqa: E402
from specs_index import criteria_by_id, criteria_for_challenge  # noqa: E402

DEFAULT_BASE_URL = "http://localhost:8000"

# The fixture the reference seed produces. Tests that rely on it skip cleanly
# when the API under test has not been seeded the same way.
SEEDED_PASSWORD = "Challenge@123"
SEEDED_USERS = {
    "john": {
        "userid": "john.doe@email.com",
        "fullname": "John Doe",
        "balance": 15491.00,
        "statement_count": 5,
    },
    "jane": {
        "userid": "jane.roe@email.com",
        "fullname": "Jane Roe",
        "balance": 4200.00,
        "statement_count": 1,
    },
}


def pytest_addoption(parser):
    group = parser.getgroup("dev-challenge harness")
    group.addoption(
        "--base-url",
        action="store",
        default=os.environ.get("BASE_URL", DEFAULT_BASE_URL),
        help=f"Base URL of the API under test (default: {DEFAULT_BASE_URL}).",
    )
    group.addoption(
        "--challenge",
        action="store",
        default=os.environ.get("CHALLENGE"),
        help="Only run criteria belonging to this challenge id.",
    )
    group.addoption(
        "--report-json",
        action="store",
        default=None,
        help="Write the scorecard as JSON to this path.",
    )
    group.addoption(
        "--report-markdown",
        action="store",
        default=None,
        help="Write the scorecard as Markdown to this path.",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "ac(id): the acceptance criterion this test verifies"
    )
    config.addinivalue_line(
        "markers", "seeded: requires the reference seed data to be present"
    )
    config._scorecard = Scorecard(
        base_url=config.getoption("--base-url"),
        challenge=config.getoption("--challenge"),
    )


def _marked_criteria(item) -> set[str]:
    """Every AC id a test declares.

    Tests stack ``@pytest.mark.ac(...)`` when one behaviour satisfies criteria in
    more than one challenge -- the fullstack track reuses the backend criteria by
    design. ``get_closest_marker`` would silently return only one of them.
    """
    return {
        marker.args[0]
        for marker in item.iter_markers("ac")
        if marker.args
    }


def pytest_collection_modifyitems(config, items):
    """Restrict the run to one challenge's criteria when --challenge is given."""
    challenge = config.getoption("--challenge")
    if not challenge:
        return

    wanted = set(criteria_for_challenge(challenge))
    kept, dropped = [], []
    for item in items:
        if wanted & _marked_criteria(item):
            kept.append(item)
        else:
            dropped.append(item)

    items[:] = kept
    config._scorecard.note_filtered(len(dropped))

    if not kept:
        raise pytest.UsageError(
            f"No harness tests are marked for challenge {challenge!r}.\n"
            "Either the challenge is verified manually (see its spec) or the "
            "harness has no coverage for it yet."
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" and not (report.when == "setup" and report.skipped):
        return

    criteria = _marked_criteria(item)
    if not criteria:
        return

    scorecard = item.config._scorecard
    if report.skipped:
        reason = ""
        if isinstance(report.longrepr, tuple) and len(report.longrepr) == 3:
            reason = str(report.longrepr[2]).removeprefix("Skipped: ")
        status, detail = "skipped", reason
    elif report.passed:
        status, detail = "passed", ""
    else:
        status, detail = "failed", _short_reason(report)

    for ac_id in criteria:
        scorecard.record(ac_id, status, detail)


def _short_reason(report) -> str:
    text = str(report.longreprtext or "").strip()
    for line in reversed(text.splitlines()):
        line = line.strip()
        if line.startswith("E "):
            return line[2:].strip()
    return text.splitlines()[-1].strip() if text else "failed"


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    scorecard: Scorecard = config._scorecard
    scorecard.print_to(terminalreporter)

    json_path = config.getoption("--report-json")
    if json_path:
        Path(json_path).write_text(scorecard.to_json(), encoding="utf-8")
        terminalreporter.write_line(f"Wrote JSON scorecard to {json_path}")

    markdown_path = config.getoption("--report-markdown")
    if markdown_path:
        Path(markdown_path).write_text(scorecard.to_markdown(), encoding="utf-8")
        terminalreporter.write_line(f"Wrote Markdown scorecard to {markdown_path}")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def base_url(pytestconfig) -> str:
    return pytestconfig.getoption("--base-url").rstrip("/")


@pytest.fixture(scope="session")
def api(base_url):
    """HTTP client pointed at the API under test."""
    with httpx.Client(base_url=base_url, timeout=15.0, follow_redirects=False) as client:
        try:
            client.get("/")
        except httpx.HTTPError as exc:
            pytest.exit(
                f"Cannot reach {base_url}: {exc}\n"
                "Is the API running? Pass --base-url if it is somewhere else.",
                returncode=2,
            )
        yield client


@pytest.fixture
def new_user(api):
    """Register a fresh user through the public API and return their credentials.

    Self-contained, so these tests work against any implementation regardless
    of what is in its database.
    """

    def _create(**overrides):
        suffix = uuid.uuid4().hex[:10]
        payload = {
            "userid": f"harness-{suffix}@example.com",
            "password": "HarnessPw@123",
            "fullname": f"Harness {suffix[:6].upper()}",
            "birthdate": "1990-05-17",
        }
        payload.update(overrides)

        response = api.post("/users/", json=payload)
        if response.status_code != 201:
            pytest.skip(
                f"Could not register a user (POST /users/ returned "
                f"{response.status_code}). Implement backend-02 first."
            )
        return payload

    return _create


@pytest.fixture
def token_for(api):
    """Log a user in and return their Bearer header."""

    def _login(userid: str, password: str) -> dict[str, str]:
        response = api.post("/auth/", json={"userid": userid, "password": password})
        if response.status_code != 200:
            pytest.skip(
                f"Could not authenticate {userid} (POST /auth/ returned "
                f"{response.status_code}). Implement backend-03 first."
            )
        return {"Authorization": f"Bearer {response.json()['access_token']}"}

    return _login


@pytest.fixture
def authed_user(new_user, token_for):
    """A freshly registered user together with their auth header."""
    user = new_user()
    return user, token_for(user["userid"], user["password"])


@pytest.fixture
def seeded(api, token_for):
    """Access a reference-seed user, skipping the test if the seed is absent."""

    def _get(which: str):
        spec = SEEDED_USERS[which]
        response = api.post(
            "/auth/", json={"userid": spec["userid"], "password": SEEDED_PASSWORD}
        )
        if response.status_code != 200:
            pytest.skip(
                f"Reference seed data not present ({spec['userid']} cannot log in). "
                "Run `python scripts/seed.py`, or provide equivalent seed data — "
                "see the challenge spec."
            )
        header = {"Authorization": f"Bearer {response.json()['access_token']}"}
        return spec, header

    return _get


@pytest.fixture
def add_statement(api):
    """Append a statement to a user's ledger, skipping if the API cannot.

    ``POST /statement/`` is how the reference API lets a client seed a ledger.
    An implementation that does not offer it cannot be checked for the balance
    arithmetic criteria, which is reported as a skip rather than a failure.
    """

    def _add(header, *, type_, amount, from_user, to_user, description="harness"):
        response = api.post(
            "/statement/",
            headers=header,
            json={
                "id": 0,
                "description": description,
                "type": type_,
                "created_at": "2024-01-01T00:00:00",
                "amount": f"{amount:.2f}",
                "from_user": from_user,
                "to_user": to_user,
                "bank_name": "Harness Bank",
                "authentication": uuid.uuid4().hex,
            },
        )
        if response.status_code not in (200, 201):
            pytest.skip(
                f"Cannot create statements (POST /statement/ returned "
                f"{response.status_code}), so balance arithmetic cannot be verified."
            )
        return response

    return _add


@pytest.fixture
def balance_of(api):
    def _balance(header) -> float:
        response = api.get("/balance/", headers=header)
        assert response.status_code == 200, f"GET /balance/ returned {response.status_code}"
        return float(response.json()["amount"])

    return _balance


@pytest.fixture(scope="session")
def criterion_text():
    """Look up a criterion's wording, for assertion messages."""

    def _text(ac_id: str) -> str:
        criterion = criteria_by_id().get(ac_id)
        return criterion.title if criterion else ac_id

    return _text
