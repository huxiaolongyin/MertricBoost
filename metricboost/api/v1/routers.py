from fastapi import APIRouter

from .asset import router as asset_router
from .auth import router as auth_router
from .collect import router as collect_router
from .metric import router as metric_router
from .report import router as report_router
from .route import router as route_router
from .system import router as system_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["权限认证"])
router.include_router(system_router, prefix="/system", tags=["系统管理"])
router.include_router(route_router, prefix="/route", tags=["路由管理"])
router.include_router(asset_router, prefix="/asset", tags=["资产管理"])
router.include_router(metric_router, prefix="/metric", tags=["指标管理"])
router.include_router(report_router, prefix="/report", tags=["报告管理"])
router.include_router(collect_router, prefix="/collect", tags=["数据采集"])
