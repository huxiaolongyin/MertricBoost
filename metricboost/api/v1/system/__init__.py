from fastapi import APIRouter

from .apis import router as api_router
from .logs import router as log_router
from .menus import router as menu_router
from .roles import router as role_router
from .users import router as user_router

router = APIRouter()

router.include_router(user_router, tags=["用户管理"])
router.include_router(role_router, tags=["角色管理"])
router.include_router(menu_router, tags=["菜单管理"])
router.include_router(api_router, tags=["接口管理"])
router.include_router(log_router, tags=["日志管理"])
