"""backend-04-statements / fullstack-03-statement — GET /statements/"""

import pytest

REQUIRED_FIELDS = {
    "id",
    "description",
    "type",
    "created_at",
    "amount",
    "from_user",
    "to_user",
    "bank_name",
    "authentication",
}


@pytest.mark.ac("BE04-AC1")
def test_unauthenticated_request_is_rejected(api):
    response = api.get("/statements/")

    assert response.status_code == 401, (
        f"GET /statements/ without a token should return 401, got {response.status_code}"
    )
    assert response.json() == {"detail": "Not authenticated"}, (
        f'expected {{"detail": "Not authenticated"}}, got {response.json()}'
    )


@pytest.mark.ac("BE04-AC2")
@pytest.mark.ac("FS03-AC1")
def test_response_has_the_documented_shape(api, seeded):
    _spec, header = seeded("john")

    response = api.get("/statements/", headers=header)

    assert response.status_code == 200, f"expected 200, got {response.status_code}"
    rows = response.json()
    assert isinstance(rows, list), f"expected a JSON array, got {type(rows).__name__}"
    assert rows, "the seeded user should have statements"

    missing = REQUIRED_FIELDS - set(rows[0])
    assert not missing, f"statement objects are missing fields: {sorted(missing)}"
    assert rows[0]["type"] in {"Deposit", "Withdrawal", "Transfer"}, (
        f"unexpected type {rows[0]['type']!r}"
    )


@pytest.mark.ac("BE04-AC3")
def test_limit_caps_the_page_size(api, seeded):
    _spec, header = seeded("john")

    response = api.get("/statements/", params={"skip": 0, "limit": 2}, headers=header)

    assert response.status_code == 200
    assert len(response.json()) == 2, (
        f"limit=2 should return exactly 2 rows, got {len(response.json())}"
    )


@pytest.mark.ac("BE04-AC4")
def test_skip_offsets_the_page(api, seeded):
    _spec, header = seeded("john")

    unskipped = api.get("/statements/", params={"skip": 0, "limit": 10}, headers=header).json()
    skipped = api.get("/statements/", params={"skip": 1, "limit": 10}, headers=header).json()

    assert len(unskipped) >= 2, "need at least two rows to check the offset"
    assert skipped[0]["id"] == unskipped[1]["id"], (
        "skip=1 should start one row later; "
        f"got id {skipped[0]['id']} where {unskipped[1]['id']} was expected"
    )


@pytest.mark.ac("BE04-AC5")
@pytest.mark.ac("FS03-AC4")
def test_results_are_scoped_to_the_caller(api, seeded):
    spec, header = seeded("john")

    rows = api.get("/statements/", params={"limit": 100}, headers=header).json()

    assert len(rows) == spec["statement_count"], (
        f"{spec['userid']} should see exactly {spec['statement_count']} statements, "
        f"got {len(rows)}. Rows belonging to other people are leaking through."
    )
    for row in rows:
        assert spec["fullname"] in (row["from_user"], row["to_user"]), (
            f"statement {row['id']} involves neither side of {spec['fullname']}: "
            f"{row['from_user']} -> {row['to_user']}"
        )


@pytest.mark.ac("BE04-AC6")
def test_a_second_user_sees_only_their_own_rows(api, seeded):
    john_spec, john_header = seeded("john")
    jane_spec, jane_header = seeded("jane")

    john_rows = api.get("/statements/", params={"limit": 100}, headers=john_header).json()
    jane_rows = api.get("/statements/", params={"limit": 100}, headers=jane_header).json()

    assert len(jane_rows) == jane_spec["statement_count"], (
        f"{jane_spec['userid']} should see {jane_spec['statement_count']} statements, "
        f"got {len(jane_rows)}"
    )

    overlap = {row["id"] for row in john_rows} & {row["id"] for row in jane_rows}
    assert not overlap, f"both users can see statements {sorted(overlap)}"


@pytest.mark.ac("BE04-AC7")
def test_out_of_range_limit_is_rejected(api, authed_user):
    _user, header = authed_user

    response = api.get("/statements/", params={"limit": 0}, headers=header)

    assert response.status_code == 422, (
        f"limit=0 is outside 1..100 and should be rejected with 422, "
        f"got {response.status_code}"
    )
