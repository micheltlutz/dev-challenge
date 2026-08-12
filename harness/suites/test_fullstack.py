"""Fullstack criteria that can be checked at the API boundary.

The rest of the fullstack criteria are UI-level and live in `harness/ui/web/`,
or are repo-inspection and are marked for manual review in the spec.
"""

import pytest


@pytest.mark.ac("FS01-AC4")
def test_cross_origin_requests_are_allowed(api, base_url):
    """A browser-served UI must be able to reach the API.

    Checks the CORS preflight rather than a plain request: that is what a browser
    actually sends before a JSON POST from another origin, and it is where a
    misconfigured API fails.
    """
    origin = "http://localhost:3000"

    preflight = api.request(
        "OPTIONS",
        "/contact/",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert preflight.status_code < 400, (
        f"the CORS preflight was rejected with {preflight.status_code}. A browser "
        f"served from {origin} could not call this API."
    )

    allowed = preflight.headers.get("access-control-allow-origin")
    assert allowed in (origin, "*"), (
        f"Access-Control-Allow-Origin is {allowed!r}; it must allow {origin} "
        "(or *) for a separately served front-end to work"
    )

    allowed_methods = (preflight.headers.get("access-control-allow-methods") or "").upper()
    assert "POST" in allowed_methods or allowed_methods == "*", (
        f"Access-Control-Allow-Methods is {allowed_methods!r} and does not permit POST"
    )
