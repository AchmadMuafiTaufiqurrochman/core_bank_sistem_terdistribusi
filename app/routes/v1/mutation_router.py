# app/routes/v1/mutation_router.py
from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import verify_api_key
from app.schemas.overbook_mutation_schema import OverbookMutationRequest
from app.schemas.online_mutation_schema import OnlineMutationRequest
from app.schemas.listmutation_schema import ListMutation
from app.schemas.refersal_schema import RefersalRequest
from app.services.overbook_mutation_service import post_overbook_transaction_service
from app.services.online_mutation_service import post_online_transaction_service
from app.services.listmutation_service import get_list_mutation_service
from app.services.refersal_service import refersal_service

router = APIRouter(prefix="/transaction", tags=["Transactions"])

@router.post("/overbook", dependencies=[Depends(verify_api_key)])
async def post_overbook_transactions(data_overbook: OverbookMutationRequest, db: AsyncSession = Depends(get_db)):
    return await post_overbook_transaction_service(db, data_overbook)

@router.post("/online", dependencies=[Depends(verify_api_key)])
async def post_online_transactions(data_online: OnlineMutationRequest, db: AsyncSession = Depends(get_db)):
    return await post_online_transaction_service(db, data_online)

@router.post("/refersal", dependencies=[Depends(verify_api_key)])
async def post_refersal_transactions(data_refersal: RefersalRequest, db: AsyncSession = Depends(get_db)):
    return await refersal_service(db, data_refersal)

@router.post("/mutationlist", dependencies=[Depends(verify_api_key)])
async def get_mutation_list(data_mutation: ListMutation, db: AsyncSession = Depends(get_db)):
    return await get_list_mutation_service(db, data_mutation)

