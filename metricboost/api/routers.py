from fastapi import APIRouter

from .v1.routers import router as v1_router

router = APIRouter()


# 健康检查
@router.get("/health", summary="健康检查")
async def health_check():
    return {"status": "healthy"}


router.include_router(v1_router, prefix="/v1")
