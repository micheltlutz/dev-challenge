from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.balance.balance_schema import Balance
from app.database.db import SessionLocal
from app.statement.statement_model import Statement
from app.dependencies.current_user import get_current_user

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/balance/", response_model=Balance, description="""
    Esta rota retorna o saldo calculado de todas as transações de um usuário.
    
    - Regra para **Depósito**: Se o usuário depositar from_user == to_user, o valor é somado ao saldo.
    - Regra para **Depósito**: Se o usuário depositar from_user != to_user, o valor é somado ao saldo.
    - Regra para **Saque**: Se o usuário sacar da sua própria conta, o valor é subtraído do saldo.
    - Regra para **Transferência**: Se o usuário transferir para sua própria conta (to_user == from_user), o valor é somado ao saldo.
    - Regra para **Transferência**: Se o usuário transferir para outra conta (to_user != from_user), o valor é subtraído do saldo.
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