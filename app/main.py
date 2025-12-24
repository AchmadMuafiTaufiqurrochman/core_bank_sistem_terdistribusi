# app/main.py
from fastapi import FastAPI, HTTPException, APIRouter
from app.routes import router_v1

app = FastAPI(title="Core Backend")

app.include_router(router_v1, prefix="/api/v1")
