from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI

from metricboost.core.crud import CRUDBase
from metricboost.logger import get_logger
from metricboost.models.asset import DataModel
from metricboost.models.enums import ReportStatus, StatisticalPeriod
from metricboost.models.metric import Metric
from metricboost.models.report import Report, ReportTemplate
from metricboost.schemas.report import ReportCreate, ReportUpdate

logger = get_logger(__name__)


class ReportController(CRUDBase[Report, ReportCreate, ReportUpdate]):
    def __init__(self):
        super().__init__(model=Report)

    async def create(self, obj_in: ReportCreate, exclude=None):
        """
        创建报告
        """
        if await self.model.filter(name=obj_in.name).first():
            raise ValueError("报告名称已存在")
        obj_in.status = ReportStatus.PROCESSING
        await super().create(obj_in, exclude)

        # 预处理数据
        processed_data = self.prepare_data_for_analysis(obj_in.data)

        # 创建报告后，触发AI服务生成报告
        await self.generate_report_async(id, processed_data)

    async def update(self, id, obj_in, exclude=None):
        return await super().update(id, obj_in, exclude)

    async def prepare_data_for_analysis(
        self,
        metric_id: int,
        data_range: List[str],
        statistical_period: StatisticalPeriod,
        report_template_id: int,
    ) -> str:
        """
        准备数据以进行分析
        """
        # TODO:从指标中，获取多维数据
        metric = await Metric.get(id=metric_id)

        # TODO:获取 prompt 模板
        report_template = await ReportTemplate.get(id=report_template_id)

        # TODO: 拼装

        return

    async def ai_service(self, query: str) -> str:
        """
        调用AI服务生成报告
        """
        # TODO:调用AI服务生成报告
        client = OpenAI(base_url="http://121.37.31.80:3001/v1", api_key="")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
        )
        return response.choices[0].message.content

    async def generate_report_async(self, report_id: int, metric: Metric):
        """
        异步生成报告
        """
        try:
            # 获取报告对象
            report = await self.get(id=report_id)
            if not report:
                logger.error(f"报告不存在: {report_id}")
                return

            # 获取指标详细数据
            metric_data = await self.get_metric_data(metric)

            # 处理数据以适合AI分析
            processed_data = self.prepare_data_for_analysis(metric_data)

            # 生成AI报告
            report_content = await self.ai_service.generate_report(
                metric_name=metric.name,
                processed_data=processed_data,
                report_type=report.report_type,
            )

            # 更新报告内容
            await self.update(
                id=report_id,
                obj_in=ReportUpdate(content=report_content, status="completed"),
            )

            logger.info(f"报告生成成功: {report_id}")

        except Exception as e:
            logger.error(f"报告生成失败: {report_id}, 错误: {str(e)}")
            # 更新报告状态为失败
            await self.update(
                id=report_id, obj_in=ReportUpdate(status="failed", error_message=str(e))
            )
