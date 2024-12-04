from fastapi import APIRouter

from .database import router as database_router
from .domain import router as topic_router
from .model import router as model_router
from .tag import router as tag_router

router_asset = APIRouter()

router_asset.include_router(database_router, tags=["数据库管理"], dependencies=[])
router_asset.include_router(topic_router, tags=["主题管理"], dependencies=[])
router_asset.include_router(model_router, tags=["数据模型管理"], dependencies=[])
router_asset.include_router(tag_router, tags=["标签管理"], dependencies=[])
