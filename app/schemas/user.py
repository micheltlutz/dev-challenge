from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    nickname: str

    class Config:
        from_attributes = True


class UserEdit(BaseModel):
    password: str = None
    email: EmailStr = None
    nickname: str = None


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    nickname: str


class UserLogin(BaseModel):
    username: str
    password: str
