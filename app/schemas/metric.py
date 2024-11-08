from typing import Annotated
from pydantic import BaseModel, Field
from typing import Optional


class MetricBase(BaseModel):
    data_model: int = Field(alias="dataModel")
    business_scope: str = Field(alias="businessScope")
    chinese_name: str = Field(alias="chineseName")
    english_name: str = Field(alias="englishName")
    alias: Optional[str] = Field(alias="alias", default=None)
    sensitivity: str = Field(alias="sensitivity")
    statistical_period: str = Field(alias="statisticalPeriod")
    chart_type: str = Field(alias="chartType")
    chart_display_date: str = Field(alias="chartDisplayDate")
    # favorite_status: str = Field(alias="favoriteStatus")
    publish_status: str = Field(alias="publishStatus")
    create_by: Annotated[str, Field(alias="createBy")] = None


class MetricCreate(MetricBase): ...


class MetricUpdate(MetricBase): ...
