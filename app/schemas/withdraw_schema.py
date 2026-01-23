from pydantic import BaseModel
from decimal import Decimal

class WithdrawRequest(BaseModel):
    account_number: str
    amount: Decimal