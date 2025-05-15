import hashlib
from typing import Any, Dict, List, Optional

from tortoise import fields

from metricboost.models.base import BaseModel, TimestampMixin
from metricboost.models.enums import AggMethod, MetricFormat, StaticType, StatusType


class DataModel(BaseModel, TimestampMixin):
    """数据模型信息"""

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=50, description="模型名称", db_index=True)
    description = fields.CharField(max_length=255, description="主题描述", null=True)
    status = fields.CharEnumField(
        enum_type=StatusType, default=StatusType.enable, description="模型状态"
    )
    table_name = fields.CharField(
        max_length=50, description="表名", null=False, db_index=True
    )
    columns_conf = fields.TextField(description="字段配置")

    # 一个模型属于一个数据库，一个数据库可以有多个模型
    database = fields.ForeignKeyField("app_system.Database", related_name="data_models")

    # 关联域
    domains = fields.ManyToManyField("app_system.Domain", related_name="data_models")

    # 关联更新人
    update_by = fields.ForeignKeyField(
        "app_system.User", related_name="updated_data_models", description="更新人"
    )
    # 创建人
    create_by = fields.ForeignKeyField(
        "app_system.User", related_name="created_data_models", description="创建人"
    )

    class Meta:
        table = "data_models"
        table_description = "数据模型信息"

    # 添加缓存机制，避免频繁解析columns_conf
    _columns_conf_cache = None
    _columns_conf_hash = None

    def _get_parsed_columns_conf(self) -> List[Dict[str, Any]]:
        """解析并返回columns_conf配置，使用缓存优化性能"""
        if not self.columns_conf:
            return []

        # 计算当前columns_conf的哈希值，用于判断是否变化
        current_hash = hashlib.md5(str(self.columns_conf).encode()).hexdigest()

        # 如果缓存存在且哈希值未变，直接返回缓存
        if self._columns_conf_cache and current_hash == self._columns_conf_hash:
            return self._columns_conf_cache

        try:
            result = eval(self.columns_conf)

            # 更新缓存和哈希值
            self._columns_conf_cache = result
            self._columns_conf_hash = current_hash

            return result
        except Exception:
            raise ValueError(f"字段配置解析错误: {self.columns_conf}")

    def _find_column_by_type(self, static_type: str) -> Optional[Dict[str, Any]]:
        """根据静态类型查找列配置

        Args:
            static_type: 要查找的静态类型

        Returns:
            Optional[Dict[str, Any]]: 匹配的列配置，如果未找到则返回 None
        """
        columns = self._get_parsed_columns_conf()
        for column in columns:
            if column.get("staticType") == static_type:
                return column
        return None

    def _find_columns_by_type(self, static_type: StaticType) -> List[Dict[str, Any]]:
        """根据静态类型查找所有匹配的列配置

        Args:
            static_type: 要查找的静态类型

        Returns:
            List[Dict[str, Any]]: 匹配的列配置列表
        """
        columns = self._get_parsed_columns_conf()
        return [column for column in columns if column.get("staticType") == static_type]

    @property
    def date_column(self) -> str:
        """获取日期列名称"""
        column = self._find_column_by_type(StaticType.Date)
        return column.get("columnName") if column else ""

    @property
    def date_format(self) -> str:
        """获取日期格式"""
        column = self._find_column_by_type(StaticType.Date)
        return column.get("format") if column else ""

    @property
    def metric_format(self) -> MetricFormat:
        """获取指标格式"""
        column = self._find_column_by_type("metric")
        return column.get("format") if column else MetricFormat.Default

    @property
    def dimension_columns(self) -> List[Dict[str, Any]]:
        """获取所有维度列名称列表"""
        dim_columns = self._find_columns_by_type(StaticType.Dimension)
        return [
            {"label": column.get("columnComment"), "value": column.get("columnName")}
            for column in dim_columns
            if column.get("columnName")
        ]

    @property
    def filter_conditions(self) -> list:
        """获取过滤条件"""
        columns = self._find_columns_by_type(StaticType.Filter)
        return [
            f"{column.get('columnName')} {column.get('extraCaculate')}"
            for column in columns
        ]

    @property
    def metric_column(self) -> str:
        """获取指标列名称"""
        column = self._find_column_by_type(StaticType.Metric)
        return column.get("columnName") if column else ""

    @property
    def agg_method(self) -> AggMethod:
        """获取聚合方法"""
        column = self._find_column_by_type(StaticType.Metric)
        return column.get("aggMethod") if column else AggMethod.Default

    @property
    def extra_caculate(self) -> str:
        """获取扩展计算"""
        column = self._find_column_by_type(StaticType.Metric)
        return column.get("extraCaculate") if column else ""

    @property
    def columns_info(self) -> Dict[str, Any]:
        """获取所有字段配置的摘要信息

        Returns:
            Dict[str, Any]: 包含日期、维度和指标信息的字典
        """
        return {
            "date": {"column": self.date_column, "format": self.date_format},
            "dimensions": self.dimension_columns,
            "metric": {
                "column": self.metric_column,
                "agg_method": self.agg_method,
                "extra_caculate": self.extra_caculate,
            },
        }
