from datetime import datetime

from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)
