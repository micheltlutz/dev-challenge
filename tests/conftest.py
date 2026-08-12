"""Test fixtures.

Every test run gets its own throwaway SQLite file, seeded by ``scripts/seed.py``
so the assertions can reference the same fixture data the specs quote.

``DATABASE_URL`` and ``SECRET`` must be set *before* ``app.config`` is imported,
which is why this module does the environment setup at import time rather than
inside a fixture.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

_TMP_DIR = tempfile.mkdtemp(prefix="dev-challenge-tests-")
_TEST_DB = Path(_TMP_DIR) / "test.db"

os.environ["DATABASE_URL"] = f"sqlite:///{_TEST_DB}"
os.environ["SECRET"] = "test-secret-not-used-anywhere-real"
os.environ["VERSION"] = "2.0.0"
os.environ["SQL_ECHO"] = "false"

from scripts.seed import (  # noqa: E402
    DEMO_PASSWORD,
    JANE_ROE_EXPECTED_BALANCE,
    JOHN_DOE_EXPECTED_BALANCE,
    build,
)

build(_TEST_DB)

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def john_doe():
    return {
        "userid": "john.doe@email.com",
        "password": DEMO_PASSWORD,
        "fullname": "John Doe",
        "balance": JOHN_DOE_EXPECTED_BALANCE,
        "statement_count": 5,
    }


@pytest.fixture(scope="session")
def jane_roe():
    return {
        "userid": "jane.roe@email.com",
        "password": DEMO_PASSWORD,
        "fullname": "Jane Roe",
        "balance": JANE_ROE_EXPECTED_BALANCE,
        "statement_count": 1,
    }


@pytest.fixture(scope="session")
def auth_header(client):
    """Return a callable that logs a demo user in and yields their Bearer header."""

    def _login(user):
        response = client.post(
            "/auth/", json={"userid": user["userid"], "password": user["password"]}
        )
        assert response.status_code == 200, response.text
        return {"Authorization": f"Bearer {response.json()['access_token']}"}

    return _login
