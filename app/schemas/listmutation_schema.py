from pydantic import BaseModel

class ListMutation(BaseModel):
    account_number: str
    start_date: str
    end_date: str
