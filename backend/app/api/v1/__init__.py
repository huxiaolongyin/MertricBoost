from fastapi import APIRouter

from .auth import router_auth
from .route import router_route
from .system_manage import router_system
from .metric import router_metric
from .asset import router_asset
from .service import router_service
from .report import router_report

v1_router = APIRouter()

v1_router.include_router(router_auth, prefix="/auth", tags=["权限认证"])
v1_router.include_router(router_route, prefix="/route", tags=["路由管理"])
v1_router.include_router(router_system, prefix="/system-manage", tags=["系统管理"])
v1_router.include_router(router_metric, prefix="/metric", tags=["指标管理"])
v1_router.include_router(router_asset, prefix="/asset", tags=["数据资产"])
v1_router.include_router(router_service, prefix="/service", tags=["数据服务"])
v1_router.include_router(router_report, tags=["报表管理"])
