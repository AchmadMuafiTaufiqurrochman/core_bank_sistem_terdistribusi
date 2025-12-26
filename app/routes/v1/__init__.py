from fastapi import APIRouter
from .mutation_router import router as mutation_router
from .portofolio_router import router as portofolio_router

router_v1 = APIRouter()
router_v1.include_router(mutation_router)
router_v1.include_router(portofolio_router)