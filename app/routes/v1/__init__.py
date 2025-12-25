from fastapi import APIRouter
from .transaction_internal_router import router as transaction_internal_router
from .portofolio_router import router as portofolio_router

router_v1 = APIRouter()
router_v1.include_router(transaction_internal_router)
router_v1.include_router(portofolio_router)