from fastapi import APIRouter

from .data_model import router as model_router
from .database import router as database_router
from .domain import router as domain_router
from .tag import router as tag_router

router = APIRouter()

router.include_router(database_router, tags=["数据库管理"])
router.include_router(domain_router, tags=["数据域管理"])
router.include_router(tag_router, tags=["数据标签管理"])
router.include_router(model_router, tags=["数据模型管理"])
