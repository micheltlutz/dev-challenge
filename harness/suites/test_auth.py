"""backend-03-login / fullstack-02-auth — POST /auth/"""

import base64
import json
import time

import pytest


def _decode_jwt(token: str):
    """Decode a JWT's header and payload without verifying the signature.

    The harness cannot know the candidate's signing secret, so it inspects the
    claims structurally rather than validating them.
    """
    parts = token.split(".")
    assert len(parts) == 3, f"not a three-part JWT: {token[:40]}..."

    def segment(raw: str):
        padded = raw + "=" * (-len(raw) % 4)
        return json.loads(base64.urlsafe_b64decode(padded))

    return segment(parts[0]), segment(parts[1])


@pytest.mark.ac("BE03-AC1")
@pytest.mark.ac("FS02-AC1")
def test_valid_credentials_return_a_token(api, new_user):
    user = new_user()

    response = api.post(
        "/auth/", json={"userid": user["userid"], "password": user["password"]}
    )

    assert response.status_code == 200, (
        f"expected 200, got {response.status_code}: {response.text[:200]}"
    )
    body = response.json()
    assert body.get("access_token"), f"no access_token in {body}"
    assert body.get("token_type") == "bearer", (
        f"expected token_type 'bearer', got {body.get('token_type')!r}"
    )


@pytest.mark.ac("BE03-AC2")
def test_wrong_password_is_rejected(api, new_user):
    user = new_user()

    response = api.post(
        "/auth/", json={"userid": user["userid"], "password": "definitely-wrong"}
    )

    assert response.status_code == 401, (
        f"a wrong password should return 401, got {response.status_code}"
    )
    assert response.json().get("detail") == "Incorrect username or password", (
        f"expected detail 'Incorrect username or password', got {response.json()}"
    )


@pytest.mark.ac("BE03-AC3")
def test_unknown_user_is_rejected_identically(api, new_user):
    user = new_user()

    wrong_password = api.post(
        "/auth/", json={"userid": user["userid"], "password": "definitely-wrong"}
    )
    unknown_user = api.post(
        "/auth/", json={"userid": "nobody-here@example.com", "password": "whatever"}
    )

    assert unknown_user.status_code == 401, (
        f"an unknown user should return 401, got {unknown_user.status_code}"
    )
    assert unknown_user.json() == wrong_password.json(), (
        "an unknown user and a wrong password must be indistinguishable, otherwise "
        "the endpoint reveals which e-mails are registered.\n"
        f"unknown user: {unknown_user.json()}\nwrong password: {wrong_password.json()}"
    )


@pytest.mark.ac("BE03-AC4")
def test_token_is_a_valid_hs256_jwt(api, new_user):
    user = new_user()
    token = api.post(
        "/auth/", json={"userid": user["userid"], "password": user["password"]}
    ).json()["access_token"]

    header, payload = _decode_jwt(token)

    assert header.get("alg") == "HS256", f"expected alg HS256, got {header.get('alg')!r}"
    assert payload.get("sub"), f"the token carries no 'sub' claim: {payload}"
    assert "exp" in payload, f"the token carries no 'exp' claim: {payload}"

    lifetime_minutes = (payload["exp"] - time.time()) / 60
    assert 25 <= lifetime_minutes <= 35, (
        f"the token should expire in about 30 minutes, got {lifetime_minutes:.1f}"
    )


@pytest.mark.ac("BE03-AC5")
def test_token_opens_a_protected_route(api, authed_user):
    _user, header = authed_user

    response = api.get("/balance/", headers=header)

    assert response.status_code == 200, (
        f"a fresh token should be accepted on GET /balance/, got {response.status_code}"
    )


@pytest.mark.ac("BE03-AC6")
def test_tampered_token_is_rejected(api, authed_user):
    _user, header = authed_user
    token = header["Authorization"].removeprefix("Bearer ")
    tampered = token[:-1] + ("A" if token[-1] != "A" else "B")

    response = api.get("/balance/", headers={"Authorization": f"Bearer {tampered}"})

    assert response.status_code == 401, (
        f"a token with an altered signature must be rejected with 401, "
        f"got {response.status_code}"
    )
