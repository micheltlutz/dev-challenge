"""backend-01-contact / fullstack-01-contact — POST /contact/"""

import pytest

VALID = {
    "name": "Ada Lovelace",
    "email": "ada@example.com",
    "message": "I would like to know more about the project.",
    "interest": "Back-end",
}


@pytest.mark.ac("BE01-AC1")
@pytest.mark.ac("FS01-AC1")
def test_valid_submission_is_accepted(api):
    response = api.post("/contact/", json=VALID)

    assert response.status_code == 200, (
        f"expected 200, got {response.status_code}: {response.text[:200]}"
    )
    body = response.json()
    assert "msg" in body, f"response has no 'msg' key: {body}"
    assert VALID["name"] in body["msg"], (
        f"the message should acknowledge the sender by name; got {body['msg']!r}"
    )


@pytest.mark.ac("BE01-AC2")
def test_missing_field_is_rejected(api):
    payload = {k: v for k, v in VALID.items() if k != "message"}
    response = api.post("/contact/", json=payload)

    assert response.status_code == 422, (
        f"a body without 'message' should be rejected with 422, got {response.status_code}"
    )


@pytest.mark.ac("BE01-AC3")
def test_malformed_email_is_rejected(api):
    response = api.post("/contact/", json={**VALID, "email": "not-an-email"})

    assert response.status_code == 422, (
        f"'not-an-email' should be rejected with 422, got {response.status_code}"
    )


@pytest.mark.ac("BE01-AC4")
def test_route_is_public(api):
    response = api.post("/contact/", json=VALID)

    assert response.status_code != 401, (
        "POST /contact/ must not require authentication"
    )
    assert response.status_code == 200
