from tortoise import fields

from metricboost.models.base import BaseModel, TimestampMixin
from metricboost.models.enums import IconType, MenuType, StatusType


class Menu(BaseModel, TimestampMixin):
    id = fields.IntField(primary_key=True, description="菜单ID")
    menu_name = fields.CharField(max_length=100, description="菜单名称")
    menu_type = fields.CharEnumField(MenuType, description="菜单类型")
    route_name = fields.CharField(max_length=100, description="路由名称")
    route_path = fields.CharField(max_length=200, description="路由路径")

    path_param = fields.CharField(null=True, max_length=200, description="路径参数")
    route_param = fields.JSONField(null=True, description="路由参数, List[dict]")
    order = fields.IntField(default=0, description="菜单顺序")
    component = fields.CharField(null=True, max_length=100, description="路由组件")

    parent_id = fields.IntField(default=0, max_length=10, description="父菜单ID")
    i18n_key = fields.CharField(
        max_length=100, description="用于国际化的展示文本，优先级高于title"
    )

    icon = fields.CharField(null=True, max_length=100, description="图标名称")
    icon_type = fields.CharEnumField(IconType, null=True, description="图标类型")

    href = fields.CharField(null=True, max_length=200, description="外链")
    multi_tab = fields.BooleanField(default=False, description="是否支持多页签")
    keep_alive = fields.BooleanField(default=False, description="是否缓存")
    hide_in_menu = fields.BooleanField(default=False, description="是否在菜单隐藏")
    active_menu = fields.CharField(
        null=True, max_length=100, description="隐藏的路由需要激活的菜单"
    )  # 枚举
    fixed_index_in_tab = fields.IntField(
        null=True, max_length=10, description="固定在页签的序号"
    )
    status = fields.CharEnumField(
        enum_type=StatusType, default=StatusType.enable, description="状态"
    )

    redirect = fields.CharField(null=True, max_length=200, description="重定向路径")
    props = fields.BooleanField(default=False, description="是否为首路由")
    constant = fields.BooleanField(default=False, description="是否为公共路由")

    buttons = fields.ManyToManyField("app_system.Button", related_name="menu_buttons")

    class Meta:
        table = "menus"
