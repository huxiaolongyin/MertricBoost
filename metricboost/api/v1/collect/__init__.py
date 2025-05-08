from fastapi import APIRouter

from .collect import router as collect_router

router = APIRouter()

router.include_router(collect_router, tags=["数据采集"])
