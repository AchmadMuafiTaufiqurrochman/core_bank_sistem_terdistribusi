from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import verify_api_key
from app.db.database import get_db
from app.services.create_portofolio_service import create_portofolio_service
from app.services.deposit_service import deposit_service
from app.schemas.create_porto_schema import RegisterRequest
from app.schemas.deposit_schema import DepositRequest

router = APIRouter(prefix="/portofolio", tags=["Portofolio"])

@router.post("/create", dependencies=[Depends(verify_api_key)])
async def create_portofolio(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    return await create_portofolio_service(db, request)

@router.post("/balance/deposit", dependencies=[Depends(verify_api_key)])
async def add_balance(request: DepositRequest, db: AsyncSession = Depends(get_db)):
    return await deposit_service(db, request)