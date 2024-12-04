from fastapi import APIRouter
from .service_api import router

router_service = APIRouter()
router_service.include_router(router,prefix="/api")
