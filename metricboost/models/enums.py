from enum import Enum
from typing import Any, Dict, List, Optional


class EnumBase(Enum):
    """
    枚举基础类

    提供枚举值和名称的获取方法
    """

    @classmethod
    def get_member_values(cls) -> List[Any]:
        """获取所有枚举成员的值"""
        return [item.value for item in cls._member_map_.values()]

    @classmethod
    def get_member_names(cls) -> List[str]:
        """获取所有枚举成员的名称"""
        return [name for name in cls._member_names_]

    @classmethod
    def get_dict(cls) -> Dict[str, Any]:
        """获取枚举名称和值的字典映射"""
        return {name: member.value for name, member in cls._member_map_.items()}

    @classmethod
    def from_value(cls, value: Any) -> Optional["EnumBase"]:
        """
        根据值获取对应的枚举成员

        Args:
            value: 枚举值

        Returns:
            Optional[EnumBase]: 匹配的枚举成员或None
        """
        for member in cls:
            if member.value == value:
                return member
        return None


class IntEnum(int, EnumBase):
    """整数枚举类"""

    pass


class StrEnum(str, EnumBase):
    """字符串枚举类"""

    pass


# 以下是具体枚举类型定义
class MethodType(StrEnum):
    """HTTP方法类型"""

    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"


class LogType(StrEnum):
    """日志类型"""

    ApiLog = "1"
    UserLog = "2"
    AdminLog = "3"
    SystemLog = "4"


class LogDetailType(StrEnum):
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
    2300-2399 决策引擎
    2400-2499 数据采集
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
    RoleGetDomains = "1508"
    RoleUpdateDomains = "1509"
    RoleGetSensitivity = "1510"
    RoleUpdateSensitivity = "1511"

    RoleGetOne = "1521"
    RoleCreateOne = "1522"
    RoleUpdateOne = "1523"
    RoleDeleteOne = "1524"
    RoleBatchDeleteOne = "1525"

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
    DataPreview = "1716"
    DataBaseBatchDeleteOne = "1717"
    TableMetadata = "1718"
    ColumnMetadata = "1719"
    AggregateData = "1720"

    DomainGet = "1721"
    DomainCreate = "1722"
    DomainUpdate = "1723"
    DomainDelete = "1724"
    DomainBatchDeleteOne = "1725"

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
    MetricGet = "1801"
    MetricCreate = "1802"
    MetricUpdate = "1803"
    MetricDelete = "1804"
    MetricBatchDeleteOne = "1805"
    MetricAddTag = "1806"
    MetricRemoveTag = "1807"

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
    ReportGet = "2001"
    ReportCreate = "2002"
    ReportUpdate = "2003"
    ReportDelete = "2004"
    ReportBatchDeleteOne = "2005"
    ReportTemplateGet = "2011"
    ReportTemplateCreate = "2012"
    ReportTemplateUpdate = "2013"
    ReportTemplateDelete = "2014"
    ReportTemplateBatchDeleteOne = "2015"

    # Ai分析(2100-2199)
    AiGet = "2101"
    AiCreate = "2102"
    AiUpdate = "2103"
    AiDelete = "2104"
    AiBatchDeleteOne = "2105"

    # 任务列表(2200-2299)
    TaskGet = "2201"
    TaskCreate = "2202"
    TaskUpdate = "2203"
    TaskDelete = "2204"
    TaskBatchDeleteOne = "2205"

    # 决策引擎(2300-2399)
    DecisionGet = "2301"
    DecisionCreate = "2302"
    DecisionUpdate = "2303"
    DecisionDelete = "2304"
    DecisionBatchDeleteOne = "2305"

    # 数据采集(2400-2499)
    CollectGet = "2401"
    CollectCreate = "2402"
    CollectUpdate = "2403"
    CollectDelete = "2404"
    CollectBatchDeleteOne = "2405"
    CollectExecute = "2406"
    CollectConfigure = "2407"

    @classmethod
    def get_group_by_prefix(cls, prefix: str) -> Dict[str, str]:
        """
        根据前缀获取分组的枚举值

        Args:
            prefix: 枚举值前缀

        Returns:
            Dict[str, str]: 匹配前缀的枚举名称和值的字典
        """
        result = {}
        for name, member in cls._member_map_.items():
            if member.value.startswith(prefix):
                result[name] = member.value
        return result


class StatusType(StrEnum):
    """状态类型"""

    enable = "1"
    disable = "0"


class GenderType(StrEnum):
    """性别类型"""

    male = "1"
    female = "2"
    unknown = "3"


class MenuType(StrEnum):
    """菜单类型"""

    catalog = "1"  # 目录
    menu = "2"  # 菜单


class IconType(StrEnum):
    """图标类型"""

    iconify = "1"
    local = "2"


class DomainType(StrEnum):
    """域类型"""

    DATA = "1"  # 数据域
    TOPIC = "2"  # 主题域


class ChartType(str, Enum):
    Default = ""
    LINE = "line"
    BAR = "bar"


class Sensitivity(str, Enum):
    HIGH = "3"
    MEDIUM = "2"
    LOW = "1"


class StatisticalPeriod(str, Enum):
    """统计周期类型"""

    daily = "daily"  # 日
    weekly = "weekly"  # 周
    monthly = "monthly"  # 月
    quarterly = "quarterly"  # 季度
    yearly = "yearly"  # 年
    cumulative = "cumulative"  # 累计


class EditMode(str, Enum):
    """编辑模式"""

    add = "add"
    edit = "edit"


class AggMethod(str, Enum):
    """聚合方法"""

    Default = ""
    Count = "count"
    Sum = "sum"
    Avg = "avg"
    Max = "max"
    Min = "min"


class StaticType(str, Enum):
    """字段类型"""

    Default = ""  # 普通字段
    Dimension = "dim"  # 维度
    Date = "date"  # 日期
    Metric = "metric"  # 指标


class MetricFormat(str, Enum):
    Default = ""
    Number = "number"
    Float = "float"
    Percent = "percent"
    Currency = "currency"


class ReportStatus(str, Enum):
    """报告状态枚举"""

    PROCESSING = "processing"  # 处理中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败


class CollectType(str, Enum):
    """采集类型"""

    BATCH = "离线"  # 批量采集
    STREAM = "实时"  # 流式采集
