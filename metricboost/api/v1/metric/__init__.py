from fastapi import APIRouter

from .metric import router

router_metric = APIRouter()
router_metric.include_router(router, tags=["指标管理"])
