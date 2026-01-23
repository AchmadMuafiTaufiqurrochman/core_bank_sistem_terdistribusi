from pydantic import BaseModel
from decimal import Decimal

class DepositRequest(BaseModel):
    account_number: str 
    amount: Decimal

class DepositResponse(BaseModel):
    message: str
    new_balance: Decimal
    account_number: str
