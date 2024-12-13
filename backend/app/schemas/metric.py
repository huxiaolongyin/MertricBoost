from typing import Annotated, Any
from pydantic import BaseModel, Field
from typing import Optional, List


class MetricBase(BaseModel):
    data_model: int = Field(alias="dataModel")
    business_scope: str = Field(alias="businessScope")
    chinese_name: str = Field(alias="chineseName")
    english_name: str = Field(alias="englishName")
    alias: Optional[str] = Field(alias="alias", default=None)
    sensitivity: str = Field(alias="sensitivity")
    statistical_period: str = Field(alias="statisticalPeriod")
    chart_type: str = Field(alias="chartType")
    chart_display_date: int = Field(alias="chartDisplayDate")
    # favorite_status: str = Field(alias="favoriteStatus")
    publish_status: str = Field(alias="publishStatus")
    create_by: Annotated[Any, Field(alias="createBy")] = None


class MetricSearch(BaseModel):
    dateRange: List | None = None
    chineseName: str | None = None
    publishStatus: str | None = None
    favoriteStatus: str | None = None
    sensitivity: str | None = None
    topicDomain: int | None = None
    dimensionDrillDown: str | None = None
    dimensionFilter: str | None = None
    comparisonOperators: str | None = None  #
    conditions: List | str | None = None
    statisticalPeriod: str | None = None
    createBy: str | None = None
    sort: str | None = None


class MetricCreate(MetricBase): ...


class MetricUpdate(MetricBase): ...
