from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import jwt
from fastapi.responses import RedirectResponse

from app.database.db import SessionLocal
from app.user.user_model import User
from app.user.user_schema import UserLogin
from app.authentication.jwt_schema import Token
from decouple import config

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(config("token_expires")))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config("secret"), algorithm=config("algorithm"))
    return encoded_jwt


@router.post("/auth/", response_model=Token)
def login_for_access_token(form_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.userid == form_data.userid).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.userid})
    return {"access_token": access_token, "token_type": "bearer"}


# Route to redirect to the /docs
@router.get("/")
def redirect_to_docs():
    response = RedirectResponse(url='/docs')
    return response


@router.get("/health-check")
def health_check():
    return {"status": "ok"}


@router.get("/version")
def health_check():
    return {"version": "1.0.0"}