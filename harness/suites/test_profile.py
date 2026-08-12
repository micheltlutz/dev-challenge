"""backend-06-profile-edit — PUT /users/{user_id}"""

import pytest


def _user_id_of(api, header, expected_email):
    """Discover the caller's numeric id via GET /users/me.

    A client cannot call ``PUT /users/{user_id}`` without knowing its own id,
    and the token carries the e-mail rather than the id -- so the API has to
    expose it somewhere. ``GET /users/me`` is that somewhere.
    """
    response = api.get("/users/me", headers=header)
    if response.status_code != 200:
        pytest.skip(
            f"GET /users/me returned {response.status_code}. A client needs some way "
            "to learn its own user id before it can edit its profile; implement "
            "/users/me (see the spec)."
        )

    body = response.json()
    assert body.get("userid") == expected_email, (
        f"/users/me returned {body.get('userid')!r} for a token belonging to "
        f"{expected_email!r}"
    )
    assert "id" in body, f"/users/me must include the numeric id, got {body}"
    return body["id"]


@pytest.mark.ac("BE06-AC8")
def test_caller_can_discover_their_own_profile(api, authed_user):
    user, header = authed_user

    unauthenticated = api.get("/users/me")
    assert unauthenticated.status_code == 401, (
        f"GET /users/me without a token should return 401, got {unauthenticated.status_code}"
    )

    response = api.get("/users/me", headers=header)

    assert response.status_code == 200, (
        f"expected 200, got {response.status_code}: {response.text[:200]}"
    )
    body = response.json()
    assert body.get("userid") == user["userid"], (
        f"expected {user['userid']}, got {body.get('userid')!r}"
    )
    assert isinstance(body.get("id"), int), (
        f"a client needs the numeric id to call PUT /users/{{id}}; got {body}"
    )
    assert body.get("fullname") == user["fullname"]
    assert '"password"' not in response.text, "the profile must not expose a password"


@pytest.mark.ac("BE06-AC1")
def test_unauthenticated_request_is_rejected(api):
    response = api.put("/users/1", json={"fullname": "Nope"})

    assert response.status_code == 401, (
        f"PUT /users/1 without a token should return 401, got {response.status_code}"
    )
    assert response.json() == {"detail": "Not authenticated"}, (
        f'expected {{"detail": "Not authenticated"}}, got {response.json()}'
    )


@pytest.mark.ac("BE06-AC2")
def test_owner_can_update_their_profile(api, authed_user):
    user, header = authed_user
    user_id = _user_id_of(api, header, user["userid"])

    response = api.put("/users/" + str(user_id), json={"fullname": "Renamed Owner"}, headers=header)

    assert response.status_code == 200, (
        f"expected 200, got {response.status_code}: {response.text[:200]}"
    )
    assert response.json().get("fullname") == "Renamed Owner", (
        f"the response should show the new name, got {response.json()}"
    )


@pytest.mark.ac("BE06-AC3")
def test_partial_update_leaves_other_fields_untouched(api, authed_user):
    user, header = authed_user
    user_id = _user_id_of(api, header, user["userid"])

    response = api.put(
        "/users/" + str(user_id), json={"fullname": "Only The Name"}, headers=header
    )

    assert response.status_code == 200
    assert str(response.json().get("birthdate")) == user["birthdate"], (
        f"birthdate should still be {user['birthdate']}, got {response.json().get('birthdate')}"
    )


@pytest.mark.ac("BE06-AC4")
def test_response_never_exposes_the_password(api, authed_user):
    user, header = authed_user
    user_id = _user_id_of(api, header, user["userid"])

    response = api.put("/users/" + str(user_id), json={"fullname": "Still Safe"}, headers=header)

    body = response.text
    assert '"password"' not in body, f"the response exposes a password field: {body[:200]}"
    assert "hashed_password" not in body, f"the response exposes the hash: {body[:200]}"
    assert user["password"] not in body, "the response leaks the clear-text password"


@pytest.mark.ac("BE06-AC5")
def test_changing_the_password_rotates_the_credential(api, authed_user):
    user, header = authed_user
    user_id = _user_id_of(api, header, user["userid"])
    new_password = "RotatedPw@456"

    updated = api.put(
        "/users/" + str(user_id), json={"password": new_password}, headers=header
    )
    assert updated.status_code == 200, f"password update failed: {updated.status_code}"

    old = api.post("/auth/", json={"userid": user["userid"], "password": user["password"]})
    assert old.status_code == 401, (
        f"the old password should stop working, got {old.status_code}"
    )

    new = api.post("/auth/", json={"userid": user["userid"], "password": new_password})
    assert new.status_code == 200, (
        f"the new password should authenticate, got {new.status_code}"
    )


@pytest.mark.ac("BE06-AC6")
def test_a_user_cannot_edit_someone_else(api, new_user, token_for):
    victim = new_user()
    attacker = new_user()

    victim_header = token_for(victim["userid"], victim["password"])
    attacker_header = token_for(attacker["userid"], attacker["password"])
    victim_id = _user_id_of(api, victim_header, victim["userid"])

    response = api.put(
        "/users/" + str(victim_id), json={"fullname": "Hijacked"}, headers=attacker_header
    )

    assert response.status_code == 403, (
        f"editing another user's profile must return 403, got {response.status_code}. "
        "A valid token is authentication, not authorization."
    )

    unchanged = api.put("/users/" + str(victim_id), json={}, headers=victim_header)
    assert unchanged.json().get("fullname") == victim["fullname"], (
        "the victim's profile was modified despite the request being rejected"
    )


@pytest.mark.ac("BE06-AC7")
def test_unknown_user_id_is_a_404(api, authed_user):
    _user, header = authed_user

    response = api.put("/users/999999", json={"fullname": "Ghost"}, headers=header)

    assert response.status_code in (403, 404), (
        f"a non-existent user id should return 404, got {response.status_code}"
    )
    assert response.status_code == 404, (
        "the API returned 403 for a user id that does not exist; it should be 404 "
        "so a client can tell 'not found' from 'not yours'"
    )
