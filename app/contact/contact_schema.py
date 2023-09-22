from pydantic import BaseModel, EmailStr


class Contact(BaseModel):
    name: str
    email: EmailStr
    message: str
    interest: str
