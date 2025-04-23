from enum import Enum
from typing import Any, Dict, List

from tortoise import fields

from metricboost.models.base import BaseModel, TimestampMixin
from metricboost.models.enums import ChartType, Sensitivity, StatisticalPeriod


class Metric(BaseModel, TimestampMixin):
    """指标信息"""

    id = fields.IntField(primary_key=True)
    metric_name = fields.CharField(max_length=100, description="指标名称")
    metric_desc = fields.CharField(max_length=500, description="指标描述/业务口径")
    statistical_period = fields.CharEnumField(StatisticalPeriod, description="统计周期")
    statistic_scope = fields.IntField(description="统计范围")
    chart_type = fields.CharEnumField(ChartType, description="图表类型")
    sensitivity = fields.CharEnumField(Sensitivity, description="敏感度")

    # 数据模型关系：一个模型可以有多个指标，一个指标属于一个模型
    data_model = fields.ForeignKeyField(
        "app_system.DataModel",
        related_name="metrics",
        description="数据模型",
    )

    # 多对多关系：指标与域
    domains = fields.ManyToManyField(
        "app_system.Domain",
        related_name="metrics",
        description="关联的域",
    )

    # 多对多关系：指标与标签
    tags = fields.ManyToManyField(
        "app_system.Tag",
        related_name="metrics",
        description="关联的标签",
    )
    update_by = fields.ForeignKeyField(
        "app_system.User",
        related_name="updated_metrics",
        description="更新人",
    )
    create_by = fields.ForeignKeyField(
        "app_system.User",
        related_name="created_metrics",
        description="创建人",
    )

    # 私有属性用于存储临时数据
    _data: Any = None
    _dimensions: List[Dict] = None
    _format: Dict = None

    class Meta:
        table = "metrics"
        table_description = "指标管理信息"

    # @property
    # def data(self) -> Any:
    #     return self._data

    # @data.setter
    # def data(self, value: Any) -> None:
    #     self._data = value

    # @property
    # def dimensions(self) -> List[Dict]:
    #     return self._dimensions

    # @dimensions.setter
    # def dimensions(self, value: List[Dict]) -> None:
    #     self._dimensions = value

    # @property
    # def format(self) -> Dict:
    #     return self._format

    # @format.setter
    # def format(self, value: Dict) -> None:
    #     self._format = value
