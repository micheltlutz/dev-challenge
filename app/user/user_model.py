from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, Date

from app.database.db import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userid = Column(String, unique=True, index=True)
    fullname = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    hashed_password = Column(String)

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

    def hash_password(self, password):
        self.hashed_password = pwd_context.hash(password)
