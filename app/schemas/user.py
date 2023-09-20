from pydantic import BaseModel
from datetime import date


class UserCreate(BaseModel):
    username: str
    password: str
    birthday: date = None
    nickname: str = None


class UserEdit(BaseModel):
    password: str = None
    birthday: date = None
    nickname: str = None


class User(BaseModel):
    id: int
    username: str
    birthday: date
    nickname: str

    class Config:
        orm_mode = True
