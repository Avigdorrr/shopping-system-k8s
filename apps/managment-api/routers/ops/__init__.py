from fastapi import APIRouter
from .routes import router as ops_routes

ops_router = APIRouter(prefix="/-")
ops_router.include_router(ops_routes)