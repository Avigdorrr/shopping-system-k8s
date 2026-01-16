from fastapi import APIRouter
from .purchases import router as purchases_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(purchases_router)