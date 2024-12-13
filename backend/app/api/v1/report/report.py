from tortoise.expressions import Q
from fastapi import APIRouter, Query
from app.schemas.base import SuccessExtra, Success, Error
from typing import List, Optional
from app.controllers.report import report_controller
from app.schemas.report import ReportCreate, ReportUpdate


router = APIRouter()


@router.get("/reports", summary="获取报告列表")
async def read_reports(
    current: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页大小"),
    reportName: Optional[str] = Query(None, description="报告名称"),
    reportType: Optional[str] = Query(None, description="报告类型"),
    status: Optional[int] = Query(None, description="状态"),
):
    """
    获取报告列表，支持分页和搜索
    """
    # 构建搜索条件
    q = Q()
    if reportName:
        q &= Q(report_name__icontains=reportName)
    if reportType:
        q &= Q(report_type=reportType)
    if status:
        q &= Q(status=status)

    total, reports = await report_controller.get_list(
        page=current,
        page_size=size,
        search=q,
        prefetch=["create_by", "metric"],
    )

    # 将结果转换为响应模型
    records = []
    for report in reports:
        report_dict = await report.to_dict(exclude_fields=["create_by_id"])
        report_dict.update(
            {
                "createBy": report.create_by.user_name,
                "metricName": report.metric.chinese_name,
            }
        )

    return SuccessExtra(
        msg="获取成功",
        data={"records": records},
        total=total,
        current=current,
        size=size,
    )


@router.get("/reports/{id}", summary="获取报告详情")
async def read_report(id: int):
    """
    根据报告 ID 获取报告详情
    """
    report = await report_controller.get(id=id)
    if not report:
        return Error(msg="报告未找到")
    report_dict = await report.to_dict(exclude_fields=["create_by_id"])
    report_dict.update(
        {
            "createBy": (await report.create_by).user_name,
            "metricName": (await report.metric).chinese_name,
        }
    )
    print(report_dict)
    return Success(msg="获取成功", data={"records": report_dict})


@router.post("/reports", summary="创建报告")
async def create_report(report_in: ReportCreate):
    """
    创建新报告
    """
    existing_report = await report_controller.get_report_by_name(report_in.report_name)
    if existing_report:
        return Error(msg="报告名称已存在")
    report = await report_controller.create(obj_in=report_in)
    return Success(msg="创建成功", data={"create_id": report.id})


@router.patch("/reports/{id}", summary="更新报告")
async def update_report(
    id: int,
    report_in: ReportUpdate,
):
    """
    更新报告
    """
    existing_report = await report_controller.get(id=id)
    if not existing_report:
        return Error(msg="报告未找到")

    report = await report_controller.update(
        id=id,
        obj_in=report_in,
    )
    return Success(msg="更新成功", data={"update_id": id})


@router.delete("/reports/{id}", summary="删除报告")
async def delete_report(
    id: int,
):
    """
    删除报告
    """
    existing_report = await report_controller.get(id=id)
    if not existing_report:
        return Error(msg="报告未找到")

    await report_controller.remove(id=id)
    return Success(msg="删除成功", data={"delete_id": id})
