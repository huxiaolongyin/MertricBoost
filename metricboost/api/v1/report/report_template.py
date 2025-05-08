from typing import Optional

from fastapi import APIRouter, Body, Depends, Path, Query
from tortoise.expressions import Q

from metricboost.controllers.report_template import report_template_controller
from metricboost.core.ctx import get_current_user_id
from metricboost.core.response import Error, Success, SuccessExtra
from metricboost.logger import get_logger, insert_log
from metricboost.models.system import LogDetailType, LogType
from metricboost.schemas.report_template import (
    ReportTemplateCreate,
    ReportTemplateUpdate,
)

logger = get_logger(__name__)

router = APIRouter()


@router.post("/report-tpl", summary="创建报告模板")
async def create_report_template(
    obj_in: ReportTemplateCreate,
    # user_id: int = Depends(get_current_user_id),
    user_id=1,
):
    try:
        obj_in.create_by_id = user_id
        obj_in.update_by_id = user_id
        report_tpl = await report_template_controller.create(obj_in=obj_in)
        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.ReportTemplateCreate,
            log_detail=f"创建报告模板: 名称={obj_in.name}",
            by_user_id=user_id,
        )
        return Success(msg="创建成功", data={"create_id": report_tpl.id})
    except Exception as e:
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.ReportTemplateCreate,
            log_detail=f"创建报告模板失败: {str(e)}",
            by_user_id=user_id,
        )
        logger.error(f"创建报告模板失败: {str(e)}")
        return Error(msg=f"创建报告模板失败: {str(e)}")


@router.patch("/report-tpl/{id}", summary="更新报告模板")
async def update_report_template(
    id: int = Path(..., description="报告模板ID"),
    obj_in: ReportTemplateUpdate = Body(..., description="报告模板更新参数"),
    user_id: int = Depends(get_current_user_id),
):
    try:
        obj_in.update_by_id = user_id
        report_tpl = await report_template_controller.update(obj_in=obj_in)
        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.ReportTemplateUpdate,
            log_detail=f"更新报告模板: 名称={obj_in.name}",
            by_user_id=user_id,
        )
        return Success(msg="更新成功", data={"update_id": report_tpl.id})
    except Exception as e:
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.ReportTemplateUpdate,
            log_detail=f"更新报告模板失败: {str(e)}",
            by_user_id=user_id,
        )
        logger.error(f"更新报告模板失败: {str(e)}")
        return Error(msg=f"更新报告模板失败: {str(e)}")


@router.delete("/report-tpl/{id}", summary="删除报告模板")
async def delete_report_template(
    id: int = Path(..., description="报告模板ID"),
    user_id: int = Depends(get_current_user_id),
):
    try:
        await report_template_controller.remove(id=id)
        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.ReportTemplateDelete,
            log_detail=f"删除报告模板: ID={id}",
            by_user_id=user_id,
        )
        return Success(msg="删除成功", data={"delete_id": id})
    except Exception as e:
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.ReportTemplateDelete,
            log_detail=f"删除报告模板失败: {str(e)}",
            by_user_id=user_id,
        )
        logger.error(f"删除报告模板失败: {str(e)}")
        return Error(msg=f"删除报告模板失败: {str(e)}")


@router.get("/report-tpl/list", summary="获取报告模板列表")
async def get_report_template_list(
    page: int = Query(1, description="页码", ge=1),
    page_size: int = Query(10, description="每页数量", ge=1, alias="pageSize"),
    name: Optional[str] = Query(None, description="模板名称"),
    user_id: int = Depends(get_current_user_id),
):
    """
    获取报告模板列表
    """
    try:
        q = Q()
        if name:
            q &= Q(name__contains=name)

        total, report_tpl_objs = await report_template_controller.get_list(
            page=page,
            page_size=page_size,
            search=q,
            prefetch=["create_by", "update_by"],
        )
        # 转换为响应格式
        records = []
        for report_tpl_obj in report_tpl_objs:
            # 构建基础数据字典
            report_tpl_dict = await report_tpl_obj.to_dict()

            # 添加关联字段
            report_tpl_dict.update(
                {
                    "updateBy": report_tpl_obj.update_by.user_name,
                    "createBy": report_tpl_obj.create_by.user_name,
                }
            )
            records.append(report_tpl_dict)
        data = {"records": records}
        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.ReportTemplateGet,
            log_detail=f"获取报告模板列表: 页码={page}, 每页={page_size}",
            by_user_id=user_id,
        )
        return SuccessExtra(msg="获取成功", data=data)
    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.ReportTemplateGet,
            log_detail=f"获取报告模板列表失败: {str(e)}",
            by_user_id=user_id,
        )
        logger.error(f"获取报告模板列表失败: {str(e)}")
        return Error(msg=f"获取报告模板列表失败: {str(e)}")


@router.get("/report-tpl/{id}", summary="获取报告模板详情")
async def get_report_template_detail(
    id: int, user_id: int = Depends(get_current_user_id)
):
    """
    获取报告模板详情
    """
    try:
        report_tpl_obj = await report_template_controller.get(id)
        if not report_tpl_obj:
            return Error(msg="报告模板不存在")
        # 转换为响应格式
        report_tpl_dict = await report_tpl_obj.to_dict()
        # 记录日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.ReportTemplateGet,
            log_detail=f"获取报告模板详情: 报告模板ID={id}",
            by_user_id=user_id,
        )
        return Success(msg="获取成功", data=report_tpl_dict)
    except Exception as e:
        # 记录错误日志
        await insert_log(
            log_type=LogType.SystemLog,
            log_detail_type=LogDetailType.ReportTemplateGet,
            log_detail=f"获取报告模板详情失败: 报告模板ID={id}, 错误={str(e)}",
            by_user_id=user_id,
        )
        logger.error(f"获取报告模板详情失败: {str(e)}")
        return Error(msg=f"获取报告模板详情失败: {str(e)}")
