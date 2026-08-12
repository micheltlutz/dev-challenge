from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.balance.balance_schema import Balance
from app.database.db import get_db
from app.dependencies.current_user import get_current_user_record
from app.statement.statement_model import Statement
from app.statement.statement_routes import statements_for
from app.user.user_model import User

router = APIRouter()

BALANCE_RULES = """
Returns the calculated balance over the authenticated user's own statements.

- **Deposit**: the amount is added to the balance.
- **Withdrawal**: the amount is subtracted from the balance.
- **Transfer** to their own account (`to_user == from_user`): the amount is added.
- **Transfer** to another account (`to_user != from_user`): the amount is subtracted.
"""


@router.get("/balance/", response_model=Balance, description=BALANCE_RULES)
def get_calculated_balance(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_record),
):
    statements = db.query(Statement).filter(statements_for(user)).all()

    amount = 0.0

    for stmt in statements:
        value = float(stmt.amount)
        if stmt.type == "Deposit":
            amount += value
        elif stmt.type == "Withdrawal":
            amount -= value
        elif stmt.type == "Transfer":
            if stmt.to_user == stmt.from_user:
                amount += value
            else:
                amount -= value

    return Balance(amount=amount)
