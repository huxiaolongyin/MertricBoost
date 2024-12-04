from fastapi import APIRouter

from app.core.dependency import DependPermission
from .apis import router as api_router
from .logs import router as log_router
from .menus import router as menu_router
from .roles import router as role_router
from .users import router as user_router


router_system = APIRouter()
router_system.include_router(
    log_router, tags=["日志管理"], dependencies=[DependPermission]
)
router_system.include_router(
    api_router, tags=["API管理"], dependencies=[DependPermission]
)
router_system.include_router(
    menu_router, tags=["菜单管理"], dependencies=[DependPermission]
)
router_system.include_router(role_router, tags=["角色管理"], dependencies=[])
router_system.include_router(user_router, tags=["用户管理"], dependencies=[])
