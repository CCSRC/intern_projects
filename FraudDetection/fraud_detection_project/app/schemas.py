from pydantic import BaseModel

class Transaction(BaseModel):
    amount: float
    transaction_type: str
    location: str
    device: str
    merchant: str
    timestamp: str
