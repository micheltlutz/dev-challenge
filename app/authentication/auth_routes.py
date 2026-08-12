from datetime import UTC, datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.authentication.jwt_schema import Token
from app.config import ALGORITHM, SECRET, TOKEN_EXPIRES
from app.database.db import get_db
from app.user.user_model import User
from app.user.user_schema import UserLogin

router = APIRouter()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)


@router.post("/auth/", response_model=Token)
def login_for_access_token(form_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.userid == form_data.userid).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"sub": user.userid})
    return {"access_token": access_token, "token_type": "bearer"}
