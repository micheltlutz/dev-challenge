from sqlalchemy import Column, Integer, String, DateTime
from app.database.db import Base


class Statement(Base):
    __tablename__ = "statement"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, unique=False)
    type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    amount = Column(String, nullable=False)
    to_user = Column(String, nullable=False)
    from_user = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    authentication = Column(String, nullable=False)
