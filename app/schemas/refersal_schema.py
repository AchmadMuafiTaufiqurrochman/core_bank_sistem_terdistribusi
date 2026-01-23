from pydantic import BaseModel

class RefersalRequest(BaseModel):
    transaction_id: int
