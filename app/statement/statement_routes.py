import random
from datetime import datetime

from faker import Faker
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.dependencies.current_user import get_current_user, get_current_user_record
from app.statement.statement_model import Statement
from app.statement.statement_schema import StatementCreate
from app.user.user_model import User

router = APIRouter()
fake = Faker()

MAX_RANDOM_STATEMENTS = 100


def statements_for(user: User):
    """Filter statements the given user takes part in, as sender or receiver.

    Statements reference people by display name, so a user's ledger is every
    row where they are the ``from_user`` or the ``to_user``.
    """
    return or_(Statement.from_user == user.fullname, Statement.to_user == user.fullname)


@router.post("/statement/", status_code=201)
def create_statement(
    statement: StatementCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    db_statement = Statement(
        description=statement.description,
        type=statement.type,
        created_at=datetime.now(),
        amount=statement.amount,
        to_user=statement.to_user,
        from_user=statement.from_user,
        bank_name=statement.bank_name,
        authentication=statement.authentication,
    )

    db.add(db_statement)
    db.commit()
    db.refresh(db_statement)

    return JSONResponse(
        content={"msg": "success"},
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/generate-random-statement/{registers_to_generate}")
def generate_random_statements(
    registers_to_generate: int = 1,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_record),
):
    """Seed the caller's ledger with random statements, for manual exploration."""
    if registers_to_generate < 1 or registers_to_generate > MAX_RANDOM_STATEMENTS:
        raise HTTPException(
            status_code=400,
            detail=f"Count must be between 1 and {MAX_RANDOM_STATEMENTS}.",
        )

    statements = []

    for _ in range(registers_to_generate):
        statement_type = random.choice(["Deposit", "Withdrawal", "Transfer"])
        # Half the rows are self-transactions so every balance rule is exercised.
        counterparty = random.choice([user.fullname, fake.name()])

        db_statement = Statement(
            description=fake.sentence(),
            type=statement_type,
            created_at=fake.date_time_this_decade(),
            amount=str(round(fake.random_number(4, True) * 0.01, 2)),
            to_user=user.fullname if statement_type != "Transfer" else counterparty,
            from_user=user.fullname,
            bank_name=fake.company(),
            authentication=fake.sha256(),
        )

        db.add(db_statement)
        statements.append(db_statement)

    db.commit()

    for stmt in statements:
        db.refresh(stmt)

    return {
        "message": f"{registers_to_generate} random statements generated and added.",
        "statements": statements,
    }


@router.get("/statements/", response_model=list[StatementCreate])
def list_statements(
    skip: int = Query(0, ge=0, description="Number of statements to skip."),
    limit: int = Query(10, ge=1, le=100, description="Number of statements to return."),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_record),
):
    """Return the authenticated user's statements, newest first."""
    return (
        db.query(Statement)
        .filter(statements_for(user))
        .order_by(Statement.created_at.desc(), Statement.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
