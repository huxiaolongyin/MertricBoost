from fastapi import APIRouter

from .report import router as report_router
from .report_template import router as report_template_router

router = APIRouter()
router.include_router(report_router, tags=["智能报告"])
router.include_router(report_template_router, tags=["报告模板"])
