import json
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from metricboost.models.enums import AggMethod, StaticType, StatusType


class ColumnConf(BaseModel):
    """字段配置"""

    column_name: str = Field(..., description="字段名称", alias="columnName")
    column_type: str = Field(..., description="字段类型", alias="columnType")
    column_comment: Optional[str] = Field(
        None, description="字段描述", alias="columnComment"
    )
    static_type: Optional[StaticType] = Field(
        None, description="字段类型。维度字段，日期字段", alias="staticType"
    )
    agg_method: Optional[AggMethod] = Field(
        None, description="统计方式", alias="aggMethod"
    )
    format: Optional[str] = Field(None, description="时间格式", alias="format")
    extra_caculate: Optional[str] = Field(
        None, description="额外附加计算", alias="extraCaculate"
    )


class DataModelBase(BaseModel):
    name: str = Field(..., description="模型名称")
    description: Optional[str] = Field(None, description="主题描述")
    table_name: str = Field(..., description="表名", alias="tableName")
    status: StatusType = Field(StatusType.enable, description="模型状态")
    columns_conf: str | List[dict | ColumnConf] = Field(
        ..., description="字段配置", alias="columnsConf"
    )
    database_id: Optional[int] = Field(
        None, description="所属数据库ID", alias="databaseId"
    )
    domain_ids: Optional[List[int]] = Field(None, description="域ID", alias="domainIds")
    update_by_id: Optional[int] = Field(None, description="更新人", alias="updateById")
    create_by_id: Optional[int] = Field(None, description="创建人", alias="createById")
    model_config = ConfigDict(populate_by_name=True)

    # 添加验证器，将字符串转换为列表
    @model_validator(mode="before")
    @classmethod
    def validate_data(cls, data: Any) -> Any:
        if (
            isinstance(data, dict)
            and "columnsConf" in data
            and isinstance(data["columnsConf"], str)
        ):

            try:
                data["columnsConf"] = json.loads(data["columnsConf"])
            except json.JSONDecodeError:
                print(data["columnsConf"])
                raise ValueError("columnsConf必须是有效的JSON字符串")

        # 新增：将列表中的None值替换为空字符串
        if (
            isinstance(data, dict)
            and "columnsConf" in data
            and isinstance(data["columnsConf"], list)
        ):
            for column in data["columnsConf"]:
                if isinstance(column, dict):
                    # 处理可能为None的可选字段
                    for key in [
                        "columnComment",
                        "staticType",
                        "aggMethod",
                        "format",
                        "extraCaculate",
                    ]:
                        if key in column and column[key] is None:
                            column[key] = ""

        return data


class DataModelCreate(DataModelBase): ...


class DataModelUpdate(DataModelBase): ...


class DataModelResponse(DataModelBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
