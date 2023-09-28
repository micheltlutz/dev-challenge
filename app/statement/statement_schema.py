from datetime import datetime

from pydantic import BaseModel


class StatementCreate(BaseModel):
    id: int
    description: str
    type: str
    created_at: datetime
    amount: str
    to_user: str
    from_user: str
    bank_name: str
    authentication: str

    class Config:
        from_attributes = True
