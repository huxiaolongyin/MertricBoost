from fastapi import APIRouter

from app.core.dependency import DependPermission
from .apis import router as api_router
from .logs import router as log_router
from .menus import router as menu_router
from .roles import router as role_router
from .users import router as user_router
from .database import router as database_router
from .topic import router as topic_router
from .data_model import router as data_model_router

router_system_manage = APIRouter()
router_system_manage.include_router(
    log_router, tags=["日志管理"], dependencies=[DependPermission]
)
router_system_manage.include_router(
    api_router, tags=["API管理"], dependencies=[DependPermission]
)
router_system_manage.include_router(
    menu_router, tags=["菜单管理"], dependencies=[DependPermission]
)
router_system_manage.include_router(role_router, tags=["角色管理"], dependencies=[])
router_system_manage.include_router(user_router, tags=["用户管理"], dependencies=[])
router_system_manage.include_router(
    database_router, tags=["数据库管理"], dependencies=[]
)
router_system_manage.include_router(topic_router, tags=["主题管理"], dependencies=[])
router_system_manage.include_router(
    data_model_router, tags=["数据模型管理"], dependencies=[]
)
