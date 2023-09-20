from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.db import SessionLocal
from ..models.user import User
from ..schemas.user import UserCreate, UserEdit

router = APIRouter()


@router.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(SessionLocal)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(username=user.username)
    new_user.hash_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/users/{user_id}", response_model=UserEdit)
def update_user(user_id: int, user_edit: UserEdit, db: Session = Depends(SessionLocal)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_edit.password:
        db_user.hash_password(user_edit.password)
    if user_edit.birthday:
        db_user.birthday = user_edit.birthday
    if user_edit.nickname:
        db_user.nickname = user_edit.nickname

    db.commit()
    db.refresh(db_user)
    return db_user
