from fastapi import APIRouter

router = APIRouter()


@router.get("/list", summary="获取报告列表")
async def get_report_list():
    pass


@router.get("/{id}", summary="获取报告详情")
async def get_report_detail():
    pass
