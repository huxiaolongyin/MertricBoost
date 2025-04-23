from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from metricboost.models.enums import ChartType, Sensitivity, StatisticalPeriod


class MetricBase(BaseModel):
    metric_name: str = Field(..., description="指标名称", alias="metricName")
    metric_desc: str = Field(..., description="指标描述", alias="metricDesc")
    data_model_id: int = Field(..., description="所属数据模型ID", alias="dataModelId")
    statistical_period: StatisticalPeriod = Field(
        ..., description="统计周期", alias="statisticalPeriod"
    )
    statistic_scope: int = Field(..., description="统计范围", alias="statisticScope")
    chart_type: ChartType = Field(..., description="图表类型", alias="chartType")
    sensitivity: Sensitivity = Field(..., description="敏感度")
    update_by_id: Optional[int] = Field(None, description="更新人", alias="updateById")
    create_by_id: Optional[int] = Field(None, description="创建人", alias="createById")

    model_config = ConfigDict(populate_by_name=True)


class MetricCreate(MetricBase):
    domain_ids: List[int] = Field([], description="关联的域IDs", alias="domainIds")
    tag_ids: List[int] = Field([], description="关联的标签IDs", alias="tagIds")


class MetricUpdate(MetricBase):
    metric_name: Optional[str] = Field(None, description="指标名称", alias="metricName")
    metric_desc: Optional[str] = Field(None, description="指标描述", alias="metricDesc")
    data_model_id: Optional[int] = Field(
        None, description="所属数据模型ID", alias="dataModelId"
    )
    statistical_period: Optional[StatisticalPeriod] = Field(
        None, description="统计周期", alias="statisticalPeriod"
    )
    statistic_scope: Optional[int] = Field(
        None, description="统计范围", alias="statisticScope"
    )
    chart_type: Optional[ChartType] = Field(
        None, description="图表类型", alias="chartType"
    )
    sensitivity: Optional[Sensitivity] = Field(None, description="敏感度")
    domain_ids: Optional[List[int]] = Field(
        None, description="关联的域IDs", alias="domainIds"
    )
    tag_ids: Optional[List[int]] = Field(
        None, description="关联的标签IDs", alias="tagIds"
    )


class MetricResponse(MetricBase):
    id: int
    domains: List[dict] = []
    tags: List[dict] = []

    model_config = ConfigDict(from_attributes=True)


class MetricListSearch(BaseModel):
    name_or_desc: Optional[str] = Field(None, alias="nameOrDesc")
    domain_id: Optional[int] = Field(None, alias="domainId")
    tag_id: Optional[int] = Field(None, alias="tagId")
    sensitivity: Optional[str] = None
    page: Optional[int] = 1
    page_size: Optional[int] = Field(10, alias="pageSize")
    sort: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class MetricDetailSearch(BaseModel):
    name: Optional[str] = None
    domain_id: Optional[int] = Field(None, alias="domainId")
    sensitivity: Optional[str] = None
    dimension_filter: Optional[str] = Field(None, alias="dimensionFilter")
    statistical_period: Optional[str] = Field(None, alias="statisticalPeriod")
    conditions: Optional[List[Any]] = None
    sort: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)
