from fastapi import APIRouter

from app.api.v1.product import router as product_router
from app.api.v1.billing import router as billing_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(product_router)
api_router.include_router(billing_router)