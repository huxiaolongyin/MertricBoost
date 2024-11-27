from fastapi import APIRouter

from .database import router as database_router
from .domain import router as topic_router
from .data_model import router as data_model_router
from .tag import router as tag_router

router_data_asset = APIRouter()

router_data_asset.include_router(database_router, tags=["数据库管理"], dependencies=[])
router_data_asset.include_router(topic_router, tags=["主题管理"], dependencies=[])
router_data_asset.include_router(
    data_model_router, tags=["数据模型管理"], dependencies=[]
)
router_data_asset.include_router(tag_router, tags=["标签管理"], dependencies=[])
