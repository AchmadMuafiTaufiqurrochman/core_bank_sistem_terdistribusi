# app/routes/v1/mutation_router.py
from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import verify_api_key
from app.schemas.overbook_mutation_schema import OverbookMutationRequest
from app.services.overbook_mutation_services import post_overbook_transaction_service

router = APIRouter(prefix="/transaction", tags=["Transactions"])

@router.post("/overbook", dependencies=[Depends(verify_api_key)])
async def post_overbook_transactions(data_overbook: OverbookMutationRequest, db: AsyncSession = Depends(get_db)):
    return await post_overbook_transaction_service(db, data_overbook)

@router.post("/online", dependencies=[Depends(verify_api_key)])
async def post_online_transactions():
    return {"message": "Online transactions endpoint"}
