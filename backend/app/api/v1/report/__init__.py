from fastapi import APIRouter
from .report import router

router_report = APIRouter()
router_report.include_router(router)
