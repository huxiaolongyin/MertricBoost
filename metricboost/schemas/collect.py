from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from metricboost.models.enums import CollectType, StatusType


class CollectBase(BaseModel):
    name: str = Field(..., description="采集任务名称")
    type: CollectType = Field(default=CollectType.BATCH, description="采集类型")
    schedule: Optional[str] = Field(None, description="Cron调度表达式")
    origin_database_id: int = Field(
        ..., description="来源数据库ID", alias="originDatabaseId"
    )
    origin_table: str = Field(..., description="来源表名")
    target_database_id: int = Field(
        ..., description="目标数据库ID", alias="targetDatabaseId"
    )
    target_table: str = Field(..., description="目标表名")
    status: StatusType = Field(default=StatusType.disable, description="状态")
    update_by_id: Optional[int] = Field(
        None, description="更新人ID", alias="updateById"
    )
    create_by_id: Optional[int] = Field(
        None, description="创建人ID", alias="createById"
    )
    model_config = ConfigDict(populate_by_name=True)


class CollectCreate(CollectBase): ...


class CollectUpdate(BaseModel):
    name: Optional[str] = Field(None, description="采集任务名称")
    type: Optional[CollectType] = Field(None, description="采集类型")
    schedule: Optional[str] = Field(None, description="Cron调度表达式")
    origin_database_id: Optional[int] = Field(
        None, description="来源数据库ID", alias="originDatabaseId"
    )
    origin_table: Optional[str] = Field(None, description="来源表名")
    target_database_id: Optional[int] = Field(
        None, description="目标数据库ID", alias="targetDatabaseId"
    )
    target_table: Optional[str] = Field(None, description="目标表名")
    status: Optional[StatusType] = Field(None, description="状态")
    update_by_id: Optional[int] = Field(
        None, description="更新人ID", alias="updateById"
    )
    model_config = ConfigDict(populate_by_name=True)
