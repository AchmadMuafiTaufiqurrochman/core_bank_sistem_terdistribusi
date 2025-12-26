from pydantic import BaseModel
from decimal import Decimal

class DepositRequest(BaseModel):
    account_number: str
    amount: Decimal
