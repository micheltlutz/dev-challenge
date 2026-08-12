"""backend-02-create-user / fullstack-02-auth — POST /users/"""

import uuid

import pytest


def _payload(**overrides):
    suffix = uuid.uuid4().hex[:10]
    base = {
        "userid": f"harness-{suffix}@example.com",
        "password": "HarnessPw@123",
        "fullname": f"Harness {suffix[:6].upper()}",
        "birthdate": "1990-05-17",
    }
    base.update(overrides)
    return base


@pytest.mark.ac("BE02-AC1")
@pytest.mark.ac("FS02-AC1")
def test_user_is_created(api):
    response = api.post("/users/", json=_payload())

    assert response.status_code == 201, (
        f"expected 201, got {response.status_code}: {response.text[:200]}"
    )
    assert response.json() == {"msg": "success"}, (
        f"expected {{'msg': 'success'}}, got {response.json()}"
    )


@pytest.mark.ac("BE02-AC2")
def test_duplicate_userid_is_rejected(api):
    payload = _payload()
    first = api.post("/users/", json=payload)
    assert first.status_code == 201, "setup: the first registration should succeed"

    second = api.post("/users/", json=payload)

    assert second.status_code == 400, (
        f"registering the same userid twice should return 400, got {second.status_code}"
    )
    assert second.json().get("detail") == "Username already registered", (
        f"expected detail 'Username already registered', got {second.json()}"
    )


@pytest.mark.ac("BE02-AC3")
def test_malformed_email_is_rejected(api):
    response = api.post("/users/", json=_payload(userid="not-an-email"))

    assert response.status_code == 422, (
        f"'not-an-email' should be rejected with 422, got {response.status_code}"
    )


@pytest.mark.ac("BE02-AC4")
def test_malformed_birthdate_is_rejected(api):
    response = api.post("/users/", json=_payload(birthdate="13/01/1988"))

    assert response.status_code == 422, (
        f"'13/01/1988' is not ISO 8601 and should be rejected with 422, "
        f"got {response.status_code}"
    )


@pytest.mark.ac("BE02-AC5")
def test_password_is_hashed_and_never_returned(api, token_for):
    payload = _payload()
    api.post("/users/", json=payload)

    header = token_for(payload["userid"], payload["password"])
    assert header, "the registered password should authenticate"

    # The password must not surface anywhere the user is represented.
    updated = api.put(
        "/users/1", json={"fullname": payload["fullname"]}, headers=header
    )
    for response in (api.get("/statements/", headers=header), updated):
        body = response.text
        assert payload["password"] not in body, (
            f"{response.request.method} {response.request.url.path} leaked the "
            "clear-text password"
        )
        assert '"password"' not in body, (
            f"{response.request.method} {response.request.url.path} exposes a "
            "'password' field"
        )


@pytest.mark.ac("BE02-AC6")
def test_route_is_public(api):
    response = api.post("/users/", json=_payload())

    assert response.status_code != 401, "POST /users/ must not require authentication"
    assert response.status_code == 201
