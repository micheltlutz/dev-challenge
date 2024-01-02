from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.balance.balance_schema import Balance
from app.database.db import SessionLocal
from app.dependencies.current_user import get_current_user
from app.statement.statement_model import Statement

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/balance/", response_model=Balance, description="""
    This route returns the calculated balance of all transactions for a user.
    
    - Rule for **Deposit**: If the user deposits from_user == to_user, the amount is added to the balance.
    - Rule for **Deposit**: If the user deposits from_user != to_user, the amount is added to the balance.
    - Rule for **Withdrawal**: If the user withdraws from their own account, the amount is subtracted from the balance.
    - Rule for **Transfer**: If the user transfers to their own account (to_user == from_user), the amount is added to the balance.
    - Rule for **Transfer**: If the user transfers to another account (to_user != from_user), the amount is subtracted from the balance.
    """)
def get_calculated_balance(db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    statements = db.query(Statement).all()

    amount = 0

    for stmt in statements:
        if (stmt.type == "Deposit" and stmt.to_user == stmt.from_user
                or stmt.type == "Deposit" and stmt.to_user != stmt.from_user):
            amount += float(stmt.amount)
        elif stmt.type == "Withdrawal":
            amount -= float(stmt.amount)
        elif stmt.type == "Transfer":
            if stmt.to_user == stmt.from_user:
                amount += float(stmt.amount)
            elif stmt.from_user != stmt.to_user:
                amount -= float(stmt.amount)

    return Balance(amount=amount)