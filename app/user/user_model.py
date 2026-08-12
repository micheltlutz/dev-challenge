import bcrypt
from sqlalchemy import Column, Date, Integer, String

from app.database.db import Base

# bcrypt silently ignores anything past 72 bytes, so we truncate explicitly
# rather than letting the backend decide.
_MAX_PASSWORD_BYTES = 72


def _encode(password: str) -> bytes:
    return password.encode("utf-8")[:_MAX_PASSWORD_BYTES]


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userid = Column(String, unique=True, index=True)
    fullname = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    hashed_password = Column(String)

    def verify_password(self, password: str) -> bool:
        if not self.hashed_password:
            return False
        try:
            return bcrypt.checkpw(_encode(password), self.hashed_password.encode("utf-8"))
        except ValueError:
            # Stored value is not a valid bcrypt hash.
            return False

    def hash_password(self, password: str) -> None:
        self.hashed_password = bcrypt.hashpw(_encode(password), bcrypt.gensalt()).decode("utf-8")
