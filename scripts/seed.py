#!/usr/bin/env python
"""Regenerate ``dev-challenge.db`` deterministically.

The seeded database is the lab's shared fixture: the challenge specs quote its
rows and the verification harness asserts against its balances. Running this
script twice must produce the same data.

Filler rows are built from fixed word lists and a seeded ``random.Random``
rather than from Faker. Faker's output for a given seed changes between major
releases, which would silently invalidate the committed fixture every time the
dependency was upgraded; the standard library's Mersenne Twister is
reproducible across Python versions.

Usage::

    python scripts/seed.py              # rewrite ./dev-challenge.db
    python scripts/seed.py --out x.db   # write somewhere else
"""

import argparse
import hashlib
import os
import random
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

RANDOM_SEED = 42

# Fixed vocabulary for the filler rows. Deliberately boring: these exist to be
# noise that must never leak into a demo user's results.
FILLER_FIRST_NAMES = [
    "Alan", "Barbara", "Carlos", "Dorothy", "Edsger", "Frances", "Grace",
    "Hedy", "Ivan", "Joan", "Katherine", "Linus", "Margaret", "Niklaus",
    "Olga", "Peter", "Radia", "Sophie", "Tim", "Ursula",
]
FILLER_LAST_NAMES = [
    "Turing", "Liskov", "Ramos", "Vaughan", "Dijkstra", "Allen", "Hopper",
    "Lamarr", "Sutherland", "Clarke", "Johnson", "Torvalds", "Hamilton",
    "Wirth", "Ladyzhenskaya", "Naur", "Perlman", "Wilson", "Berners-Lee",
    "Franklin",
]
FILLER_BANKS = [
    "Northwind Bank", "Cascade Credit", "Ironbridge Savings", "Lakeside Trust",
    "Meridian Financial", "Copperfield Bank", "Harborview Credit Union",
]
FILLER_DESCRIPTIONS = [
    "Monthly subscription", "Grocery shopping", "Utility bill", "Book store",
    "Train ticket", "Coffee shop", "Gym membership", "Cinema tickets",
    "Pharmacy", "Hardware store", "Restaurant", "Parking fee",
]

# Known credentials, documented in the specs so challengers can log in.
DEMO_PASSWORD = "Challenge@123"

DEMO_USERS = [
    {
        "userid": "john.doe@email.com",
        "fullname": "John Doe",
        "birthdate": date(1988, 1, 13),
    },
    {
        "userid": "jane.roe@email.com",
        "fullname": "Jane Roe",
        "birthdate": date(1991, 7, 4),
    },
]

# John Doe's ledger is hand-written so that every balance rule is exercised
# exactly once and the expected total is a round, quotable number.
#
#   +15000.00  Deposit
#     -250.00  Withdrawal
#    +1200.50  Transfer to self
#     -800.25  Transfer to another account
#     +340.75  Deposit received from someone else
#   ----------
#    15491.00
JOHN_DOE_LEDGER = [
    {
        "description": "Payment from Freela",
        "type": "Deposit",
        "created_at": datetime(2023, 9, 21, 18, 46, 45),
        "amount": "15000.00",
        "from_user": "John Doe",
        "to_user": "John Doe",
        "bank_name": "Adams LLC",
    },
    {
        "description": "ATM withdrawal",
        "type": "Withdrawal",
        "created_at": datetime(2023, 9, 22, 9, 15, 0),
        "amount": "250.00",
        "from_user": "John Doe",
        "to_user": "John Doe",
        "bank_name": "Adams LLC",
    },
    {
        "description": "Moved from savings",
        "type": "Transfer",
        "created_at": datetime(2023, 9, 23, 11, 5, 30),
        "amount": "1200.50",
        "from_user": "John Doe",
        "to_user": "John Doe",
        "bank_name": "Adams LLC",
    },
    {
        "description": "Rent split",
        "type": "Transfer",
        "created_at": datetime(2023, 9, 24, 20, 40, 10),
        "amount": "800.25",
        "from_user": "John Doe",
        "to_user": "Marie Curie",
        "bank_name": "Adams LLC",
    },
    {
        "description": "Refund from Grace",
        "type": "Deposit",
        "created_at": datetime(2023, 9, 25, 14, 22, 55),
        "amount": "340.75",
        "from_user": "Grace Hopper",
        "to_user": "John Doe",
        "bank_name": "Hopper Bank",
    },
]

JOHN_DOE_EXPECTED_BALANCE = 15491.00

# Jane Roe gets a single deposit, so a second account proves that balances and
# statement lists are scoped per user.
JANE_ROE_LEDGER = [
    {
        "description": "Salary",
        "type": "Deposit",
        "created_at": datetime(2023, 9, 20, 8, 0, 0),
        "amount": "4200.00",
        "from_user": "Acme Corp",
        "to_user": "Jane Roe",
        "bank_name": "Roe Savings",
    },
]

JANE_ROE_EXPECTED_BALANCE = 4200.00

# Rows belonging to nobody in the demo set. They must never show up in either
# user's statement list -- that is what makes the scoping tests meaningful.
NOISE_ROWS = 40


def deterministic_authentication(index: int) -> str:
    """Stable stand-in for a bank authentication code."""
    return hashlib.sha256(f"dev-challenge-statement-{index}".encode()).hexdigest()


def filler_name(rng: random.Random) -> str:
    return f"{rng.choice(FILLER_FIRST_NAMES)} {rng.choice(FILLER_LAST_NAMES)}"


def build(out_path: Path) -> None:
    os.environ["DATABASE_URL"] = f"sqlite:///{out_path}"
    # Import only after DATABASE_URL is set: app.config reads it at import time.
    from app.database.db import Base, SessionLocal, engine
    from app.statement.statement_model import Statement
    from app.user.user_model import User

    if out_path.exists():
        out_path.unlink()

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    rng = random.Random(RANDOM_SEED)
    epoch = datetime(2020, 1, 1)

    try:
        for spec in DEMO_USERS:
            user = User(
                userid=spec["userid"],
                fullname=spec["fullname"],
                birthdate=spec["birthdate"],
            )
            user.hash_password(DEMO_PASSWORD)
            db.add(user)

        index = 0
        for row in JOHN_DOE_LEDGER + JANE_ROE_LEDGER:
            index += 1
            db.add(Statement(authentication=deterministic_authentication(index), **row))

        for _ in range(NOISE_ROWS):
            index += 1
            sender = filler_name(rng)
            receiver = filler_name(rng)
            while receiver == sender:
                receiver = filler_name(rng)

            db.add(
                Statement(
                    description=rng.choice(FILLER_DESCRIPTIONS),
                    type=rng.choice(["Deposit", "Withdrawal", "Transfer"]),
                    created_at=epoch + timedelta(
                        days=rng.randrange(0, 1340), minutes=rng.randrange(0, 1440)
                    ),
                    amount=f"{rng.randrange(100, 999999) / 100:.2f}",
                    from_user=sender,
                    to_user=receiver,
                    bank_name=rng.choice(FILLER_BANKS),
                    authentication=deterministic_authentication(index),
                )
            )

        db.commit()

        # The scoping criteria are only meaningful if the filler rows belong to
        # nobody. A name collision would make BE04-AC5 and BE05-AC3 pass or fail
        # for the wrong reason, so assert it rather than trusting the word lists.
        demo_names = {spec["fullname"] for spec in DEMO_USERS}
        leaked = (
            db.query(Statement)
            .filter(
                Statement.id > len(JOHN_DOE_LEDGER) + len(JANE_ROE_LEDGER),
                Statement.from_user.in_(demo_names) | Statement.to_user.in_(demo_names),
            )
            .count()
        )
        if leaked:
            raise SystemExit(
                f"{leaked} filler statement(s) name a demo user. The fixture would "
                "no longer prove per-user scoping. Adjust the filler word lists."
            )
    finally:
        db.close()

    print(f"Seeded {out_path}")
    print(f"  users:      {len(DEMO_USERS)} (password for all: {DEMO_PASSWORD})")
    print(f"  statements: {index}")
    print(f"  John Doe expected balance: {JOHN_DOE_EXPECTED_BALANCE:.2f}")
    print(f"  Jane Roe expected balance: {JANE_ROE_EXPECTED_BALANCE:.2f}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default=str(REPO_ROOT / "dev-challenge.db"),
        help="Path of the SQLite file to write (default: ./dev-challenge.db)",
    )
    args = parser.parse_args()
    build(Path(args.out).resolve())


if __name__ == "__main__":
    main()
