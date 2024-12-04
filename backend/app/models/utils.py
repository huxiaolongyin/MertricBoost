from datetime import datetime
from enum import Enum
from uuid import UUID

from tortoise import models, fields

from app.settings import APP_SETTINGS
from app.utils.tools import to_lower_camel_case


class BaseModel(models.Model):
    async def to_dict(
        self,
        include_fields: list[str] | None = None,
        exclude_fields: list[str] | None = None,
        m2m: bool = False,
    ):
        """
        将将模型对象转换为字典，模型对象的属性名将转换为小驼峰命名法
        """
        include_fields = include_fields or []
        exclude_fields = exclude_fields or []

        d = {}
        for field in self._meta.db_fields:
            if (not include_fields or field in include_fields) and (
                not exclude_fields or field not in exclude_fields
            ):
                value = getattr(self, field)
                if isinstance(value, datetime):
                    value = value.strftime(APP_SETTINGS.DATETIME_FORMAT)
                elif isinstance(value, UUID):
                    value = str(value)
                d[to_lower_camel_case(field)] = value

        if m2m:
            for field in self._meta.m2m_fields:
                if (not include_fields or field in include_fields) and (
                    not exclude_fields or field not in exclude_fields
                ):
                    values = [
                        value for value in await getattr(self, field).all().values()
                    ]
                    for value in values:
                        _value = value.copy()
                        for k, v in _value.items():
                            if isinstance(v, datetime):
                                v = v.strftime(APP_SETTINGS.DATETIME_FORMAT)
                            elif isinstance(v, UUID):
                                v = str(v)
                            value.pop(k)
                            value[to_lower_camel_case(k)] = v
                    d[to_lower_camel_case(field)] = values
        return d

    class Meta:
        abstract = True


class TimestampMixin:
    create_time = fields.DatetimeField(auto_now_add=True, use_tz=True)
    update_time = fields.DatetimeField(auto_now=True, use_tz=True)


class EnumBase(Enum):
    @classmethod
    def get_member_values(cls):
        return [item.value for item in cls._member_map_.values()]

    @classmethod
    def get_member_names(cls):
        return [name for name in cls._member_names_]


class IntEnum(int, EnumBase): ...


class StrEnum(str, EnumBase): ...


class MethodType(str, Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"


class LogType(str, Enum):
    ApiLog = "1"
    UserLog = "2"
    AdminLog = "3"
    SystemLog = "4"


class LogDetailType(str, Enum):
    """
    1000-1999 内置
    1100-1199 系统
    1200-1299 用户
    1300-1399 API
    1400-1499 菜单
    1500-1599 角色
    1600-1699 用户
    1700-1799 数据资产
    1800-1899 指标
    1900-1999 数据服务
    2000-2099 报告
    2100-2199 Ai分析
    2200-2299 任务列表
    """
    # 系统(1100-1199)
    SystemStart = "1101"
    SystemStop = "1102"

    # 用户(1200-1299)
    UserLoginSuccess = "1201"
    UserAuthRefreshTokenSuccess = "1202"
    UserLoginGetUserInfo = "1203"
    UserLoginUserNameVaild = "1211"
    UserLoginErrorPassword = "1212"
    UserLoginForbid = "1213"

    # API(1300-1399)
    ApiGetList = "1301"
    ApiGetTree = "1302"
    ApiRefresh = "1303"
    
    ApiGetOne = "1311"
    ApiCreateOne = "1312"
    ApiUpdateOne = "1313"
    ApiDeleteOne = "1314"
    ApiBatchDelete = "1315"

    # 菜单(1400-1499)
    MenuGetList = "1401"
    MenuGetTree = "1402"
    MenuGetPages = "1403"
    MenuGetButtonsTree = "1404"

    MenuGetOne = "1411"
    MenuCreateOne = "1412"
    MenuUpdateOne = "1413"
    MenuDeleteOne = "1414"
    MenuBatchDeleteOne = "1415"

    # 角色(1500-1599)
    RoleGetList = "1501"
    RoleGetMenus = "1502"
    RoleUpdateMenus = "1503"
    RoleGetButtons = "1504"
    RoleUpdateButtons = "1505"
    RoleGetApis = "1506"
    RoleUpdateApis = "1507"

    RoleGetOne = "1511"
    RoleCreateOne = "1512"
    RoleUpdateOne = "1513"
    RoleDeleteOne = "1514"
    RoleBatchDeleteOne = "1515"

    # 用户(1600-1699)
    UserGetList = "1601"
    UserGetOne = "1611"
    UserCreateOne = "1612"
    UserUpdateOne = "1613"
    UserDeleteOne = "1614"
    UserBatchDeleteOne = "1615"

    # 数据资产(1700-1799)
    DataBaseGet = "1711"
    DataBaseCreate = "1712"
    DataBaseUpdate = "1713"
    DataBaseDelete = "1714"
    DataBaseTest = "1715"
    DataBaseBatchDeleteOne = "1716"

    DataDomainGet = "1721"
    DataDomainCreate = "1722"
    DataDomainUpdate = "1723"
    DataDomainDelete = "1724"
    DataDomainBatchDeleteOne = "1725"

    TopicDomainGet = "1731"
    TopicDomainCreate = "1732"
    TopicDomainUpdate = "1733"
    TopicDomainDelete = "1734"
    TopicDomainBatchDeleteOne = "1735"

    DataModelGet = "1741"
    DataModelCreate = "1742"
    DataModelUpdate = "1743"
    DataModelDelete = "1744"
    DataModelBatchDeleteOne = "1745"

    TagGet = "1751"
    TagCreate = "1752"
    TagUpdate = "1753"
    TagDelete = "1754"
    TagBatchDeleteOne = "1755"

    # 指标(1800-1899)
    MetricTagGet = "1801"
    MetricTagCreate = "1802"
    MetricTagUpdate = "1803"
    MetricTagDelete = "1804"
    MetricTagBatchDeleteOne = "1805"

    # 数据服务(1900-1999)
    ServiceAppGet = "1901"
    ServiceAppCreate = "1902"
    ServiceAppUpdate = "1903"
    ServiceAppDelete = "1904"
    ServiceAppBatchDeleteOne = "1905"

    ServiceApiGet = "1911"
    ServiceApiCreate = "1912"
    ServiceApiUpdate = "1913"
    ServiceApiDelete = "1914"
    ServiceApiBatchDeleteOne = "1915"
    # 报告(2000-2099)

    # Ai分析(2100-2199)

    # 任务列表(2200-2299)


class StatusType(str, Enum):
    enable = "1"
    disable = "2"


class GenderType(str, Enum):
    male = "1"
    female = "2"
    unknow = "3"  # Soybean上没有


class MenuType(str, Enum):
    catalog = "1"  # 目录
    menu = "2"  # 菜单


class IconType(str, Enum):
    iconify = "1"
    local = "2"


__all__ = [
    "BaseModel",
    "TimestampMixin",
    "EnumBase",
    "IntEnum",
    "StrEnum",
    "MethodType",
    "LogType",
    "LogDetailType",
    "StatusType",
    "GenderType",
    "MenuType",
    "IconType",
]
