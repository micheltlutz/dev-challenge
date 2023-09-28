from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.dependencies.current_user import get_current_user
from app.user.user_model import User
from app.user.user_schema import UserCreate, UserEdit

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new user
@router.post("/users/", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.userid == user.userid).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(userid=user.userid)
    new_user.hash_password(user.password)
    new_user.fullname = user.fullname
    new_user.birthdate = user.birthdate

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(
        content={'msg': 'success'},
        status_code=status.HTTP_201_CREATED
    )


@router.put("/users/{user_id}", response_model=UserEdit)
def update_user(user_id: int, user_edit: UserEdit, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_edit.password:
        db_user.hash_password(user_edit.password)
    if user_edit.fullname:
        db_user.fullname = user_edit.fullname
    if user_edit.birthdate:
        db_user.birthdate = user_edit.birthdate

    db.commit()
    db.refresh(db_user)
    return db_user
