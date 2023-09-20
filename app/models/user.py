from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    birthday = Column(Date, index=True, nullable=True)
    nickname = Column(String, index=True, nullable=True)
    hashed_password = Column(String)

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

    def hash_password(self, password):
        self.hashed_password = pwd_context.hash(password)
