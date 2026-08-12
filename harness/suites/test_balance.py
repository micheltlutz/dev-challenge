"""backend-05-balance / fullstack-03-statement — GET /balance/"""

import pytest

TOLERANCE = 0.01


@pytest.mark.ac("BE05-AC1")
def test_unauthenticated_request_is_rejected(api):
    response = api.get("/balance/")

    assert response.status_code == 401, (
        f"GET /balance/ without a token should return 401, got {response.status_code}"
    )
    assert response.json() == {"detail": "Not authenticated"}, (
        f'expected {{"detail": "Not authenticated"}}, got {response.json()}'
    )


@pytest.mark.ac("BE05-AC2")
def test_balance_is_returned_as_a_number(api, authed_user):
    _user, header = authed_user

    response = api.get("/balance/", headers=header)

    assert response.status_code == 200, f"expected 200, got {response.status_code}"
    body = response.json()
    assert "amount" in body, f"response has no 'amount' key: {body}"
    assert isinstance(body["amount"], int | float), (
        f"'amount' should be a number, got {type(body['amount']).__name__}"
    )


@pytest.mark.ac("BE05-AC3")
@pytest.mark.ac("FS03-AC3")
def test_seeded_balance_is_exact(api, seeded, balance_of):
    spec, header = seeded("john")

    amount = balance_of(header)

    assert abs(amount - spec["balance"]) < TOLERANCE, (
        f"{spec['userid']} should have a balance of {spec['balance']:.2f}, got {amount:.2f}.\n"
        "Check the fold: Deposit adds, Withdrawal subtracts, Transfer to self adds, "
        "Transfer to another subtracts -- over this user's statements only."
    )


@pytest.mark.ac("BE05-AC4")
@pytest.mark.ac("FS03-AC4")
@pytest.mark.ac("FS03-AC6")
def test_balance_is_scoped_per_user(api, seeded, balance_of):
    john_spec, john_header = seeded("john")
    jane_spec, jane_header = seeded("jane")

    john_amount = balance_of(john_header)
    jane_amount = balance_of(jane_header)

    assert abs(jane_amount - jane_spec["balance"]) < TOLERANCE, (
        f"{jane_spec['userid']} should have a balance of {jane_spec['balance']:.2f}, "
        f"got {jane_amount:.2f}"
    )
    assert abs(john_amount - jane_amount) > TOLERANCE, (
        "both users report the same balance, so the balance is being computed over "
        "every statement in the database instead of the caller's own"
    )


@pytest.mark.ac("BE05-AC5")
def test_deposit_increases_the_balance(authed_user, add_statement, balance_of):
    user, header = authed_user
    before = balance_of(header)

    add_statement(
        header,
        type_="Deposit",
        amount=100.00,
        from_user=user["fullname"],
        to_user=user["fullname"],
    )

    assert abs(balance_of(header) - (before + 100.00)) < TOLERANCE, (
        f"a Deposit of 100.00 should raise the balance from {before:.2f} to "
        f"{before + 100:.2f}, got {balance_of(header):.2f}"
    )


@pytest.mark.ac("BE05-AC6")
def test_withdrawal_decreases_the_balance(authed_user, add_statement, balance_of):
    user, header = authed_user
    before = balance_of(header)

    add_statement(
        header,
        type_="Withdrawal",
        amount=100.00,
        from_user=user["fullname"],
        to_user=user["fullname"],
    )

    assert abs(balance_of(header) - (before - 100.00)) < TOLERANCE, (
        f"a Withdrawal of 100.00 should lower the balance from {before:.2f} to "
        f"{before - 100:.2f}, got {balance_of(header):.2f}"
    )


@pytest.mark.ac("BE05-AC7")
def test_transfer_to_self_adds_to_another_subtracts(authed_user, add_statement, balance_of):
    user, header = authed_user
    before = balance_of(header)

    add_statement(
        header,
        type_="Transfer",
        amount=100.00,
        from_user=user["fullname"],
        to_user=user["fullname"],
    )
    after_self = balance_of(header)
    assert abs(after_self - (before + 100.00)) < TOLERANCE, (
        f"a Transfer to one's own account should add: expected {before + 100:.2f}, "
        f"got {after_self:.2f}"
    )

    add_statement(
        header,
        type_="Transfer",
        amount=100.00,
        from_user=user["fullname"],
        to_user="Someone Else",
    )
    after_other = balance_of(header)
    assert abs(after_other - before) < TOLERANCE, (
        f"a Transfer to another account should subtract, returning to {before:.2f}, "
        f"got {after_other:.2f}"
    )
