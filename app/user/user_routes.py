from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.dependencies.current_user import get_current_user, get_current_user_record
from app.user.user_model import User
from app.user.user_schema import UserCreate, UserEdit, UserPublic

router = APIRouter()


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
        content={"msg": "success"},
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/users/me",
    response_model=UserPublic,
    description=(
        "The authenticated user's own profile. A client needs this to learn its "
        "`id` before it can call `PUT /users/{user_id}` -- the token carries the "
        "e-mail, not the numeric id."
    ),
)
def read_current_user(user: User = Depends(get_current_user_record)):
    return user


@router.put("/users/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int,
    user_edit: UserEdit,
    db: Session = Depends(get_db),
    current_userid: str = Depends(get_current_user),
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.userid != current_userid:
        raise HTTPException(
            status_code=403, detail="You can only edit your own profile"
        )

    if user_edit.password:
        db_user.hash_password(user_edit.password)
    if user_edit.fullname:
        db_user.fullname = user_edit.fullname
    if user_edit.birthdate:
        db_user.birthdate = user_edit.birthdate

    db.commit()
    db.refresh(db_user)
    return db_user
