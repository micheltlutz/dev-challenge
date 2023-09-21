from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.statement.statement_model import Statement
from app.statement.statement_schema import StatementCreate

from faker import Faker
import random

from datetime import datetime


router = APIRouter()
fake = Faker()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new statement
@router.post("/statement/", status_code=201)
def create_statement(statement: StatementCreate, db: Session = Depends(get_db)):
    # Criar o registro de statement
    db_statement = Statement(
        description=statement.description,
        type=statement.type,
        created_at=datetime.now(),
        amount=statement.amount,
        to_user=statement.to_user,
        from_user=statement.from_user,
        bank_name=statement.bank_name,
        authentication=statement.authentication
    )

    # Adicionar ao banco de dados
    db.add(db_statement)
    db.commit()
    db.refresh(db_statement)

    return JSONResponse(
        content={'msg': 'success'},
        status_code=status.HTTP_201_CREATED
    )


@router.get("/generate-random-statement/{registers_to_generate}")
def generate_random_statements(registers_to_generate: int = 1, db: Session = Depends(get_db)):
    if registers_to_generate < 1 | registers_to_generate > 100:
        raise HTTPException(status_code=400, detail="Count must be greater than 0 an minor 100.")

    statements = []

    for _ in range(registers_to_generate):
        # Gerar dados aleatórios para o statement
        description = fake.sentence()
        type = random.choice(["Deposit", "Withdrawal", "Transfer"])
        amount = str(round(fake.random_number(4, True) * 0.01, 2))  # Gera um valor aleatório como 1234.56
        to_user = fake.name()
        from_user = fake.name()
        bank_name = fake.company()
        authentication = fake.sha256()

        # Criar o registro de statement
        db_statement = Statement(
            description=description,
            type=type,
            created_at=fake.date_this_decade(),
            amount=amount,
            to_user=to_user,
            from_user=from_user,
            bank_name=bank_name,
            authentication=authentication
        )

        # Adicionar ao banco de dados
        db.add(db_statement)
        statements.append(db_statement)

    db.commit()

    for stmt in statements:
        db.refresh(stmt)

    return {"message": f"{registers_to_generate} random statements generated and added.", "statements": statements}


@router.get("/statements/")
def list_statements(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Query the database
    statements = db.query(Statement).offset(skip).limit(limit).all()
    return statements