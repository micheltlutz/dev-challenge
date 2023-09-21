from pydantic import BaseModel


class Balance(BaseModel):
    amount: float

