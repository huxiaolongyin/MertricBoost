from typing import List, Optional

from metricboost.core.crud import CRUDBase
from metricboost.core.ctx import get_current_user_id
from metricboost.logger import get_logger
from metricboost.models.report.report_template import ReportTemplate
from metricboost.schemas.report_template import (
    ReportTemplateCreate,
    ReportTemplateUpdate,
)

logger = get_logger(__name__)


class ReportTemplateController(
    CRUDBase[ReportTemplate, ReportTemplateCreate, ReportTemplateUpdate]
):
    def __init__(self):
        super().__init__(model=ReportTemplate)

    async def create(self, obj_in: ReportTemplateCreate, exclude=None):
        """
        创建报告模板
        """
        if await self.model.filter(name=obj_in.name).first():
            raise ValueError("报告模板名称已存在")

        # 创建数据模型
        return await super().create(obj_in=obj_in, exclude=exclude)

    async def update(self, id: int, obj_in: ReportTemplateUpdate, exclude=None):
        """
        更新报告模板
        """
        # 检查报告模板是否存在
        template = await self.get(id=id)
        if not template:
            raise ValueError("报告模板不存在")

        # 检查模板名称是否重复
        if (
            obj_in.name
            and await self.model.filter(name=obj_in.name).exclude(id=id).first()
        ):
            raise ValueError("报告模板名称已存在")

        # 获取当前用户ID
        current_user_id = get_current_user_id()

        # 设置更新人
        obj_in.update_by_id = current_user_id

        # 更新报告模板
        return await super().update(id=id, obj_in=obj_in, exclude=exclude)

    async def remove(self, id: int):
        """
        删除报告模板
        """
        # 检查报告模板是否存在
        template = await self.get(id=id)
        if not template:
            raise ValueError("报告模板不存在")
        # 检查该模板是否被引用
        # 注：如果有Report模型引用了模板，应该添加相关检查逻辑
        # 例如：reports_count = await Report.filter(template_id=id).count()
        # if reports_count > 0:
        #     raise ValueError(f"该模板已被{reports_count}个报告使用，无法删除")

        # 删除报告模板
        return await super().remove(id=id)


report_template_controller = ReportTemplateController()
