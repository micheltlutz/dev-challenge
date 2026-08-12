from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    userid: EmailStr
    password: str
    fullname: str
    birthdate: date

    model_config = ConfigDict(from_attributes=True)


class UserEdit(BaseModel):
    """Editable fields. Every field is optional -- only what is sent is applied."""

    password: str | None = None
    fullname: str | None = None
    birthdate: date | None = None


class UserPublic(BaseModel):
    """User representation safe to return over the wire -- never includes a password."""

    id: int
    userid: EmailStr
    fullname: str
    birthdate: date

    model_config = ConfigDict(from_attributes=True)


class User(UserPublic):
    pass


class UserLogin(BaseModel):
    userid: str
    password: str
