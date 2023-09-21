from pydantic import BaseModel, EmailStr
from datetime import date

class UserCreate(BaseModel):
    userid: EmailStr
    password: str
    fullname: str
    birthdate: date

    class Config:
        from_attributes = True


class UserEdit(BaseModel):
    password: str = None
    fullname: str = None
    birthdate: date = None


class User(BaseModel):
    id: int
    userid: EmailStr
    fullname: str
    birthdate: date


class UserLogin(BaseModel):
    userid: str
    password: str
