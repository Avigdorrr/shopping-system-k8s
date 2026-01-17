from fastapi import APIRouter
from .buys import router as purchases_router

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(purchases_router)
