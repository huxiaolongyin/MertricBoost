from fastapi import APIRouter
from .service_api import router as api_router
from .service_app import router as app_router

router_service = APIRouter()
router_service.include_router(api_router, prefix="/api")
router_service.include_router(app_router)