from metricboost.core.security import get_password_hash
from metricboost.logger import get_logger
from metricboost.models.asset import Database, DataModel, Domain, Tag
from metricboost.models.metric import Metric
from metricboost.models.system import Api, Button, Menu, Role, User

logger = get_logger(__name__)


async def load_role_data():
    """加载角色数据"""
    logger.debug("开始加载角色数据")
    try:
        await Role.create(role_name="普通用户", role_code="user")
        await Role.create(role_name="超级管理员", role_code="R_SUPER")
        logger.debug("角色数据加载成功")
    except Exception as e:
        logger.error("加载角色数据时发生异常: %s", e)
        raise e


async def load_user_data():
    """加载用户数据"""
    logger.debug("开始加载用户数据")
    try:
        user1 = await User.create(
            user_name="admin",
            password=get_password_hash("admin"),
        )
        role_obj = await Role.get(role_code="user")
        await user1.roles.add(role_obj)

        user2 = await User.create(
            user_name="super_admin",
            password=get_password_hash("admin"),
        )
        role_obj = await Role.get(role_code="R_SUPER")
        await user2.roles.add(role_obj)
        # 添加关系

        logger.debug("用户数据加载成功")
    except Exception as e:
        logger.error("加载用户数据时发生异常: %s", e)
        raise e


async def load_button_data():
    """加载按钮数据"""
    logger.debug("开始加载按钮数据")
    try:
        await Button.create(
            button_name="新增",
            button_code="add",
            button_desc="新增按钮",
        )
        await Button.create(
            button_name="更新",
            button_code="update",
            button_desc="更新按钮",
        )
        await Button.create(
            button_name="删除",
            button_code="delete",
            button_desc="删除按钮",
        )
        logger.debug("按钮数据加载成功")
    except Exception as e:
        logger.error("加载按钮数据时发生异常: %s", e)
        raise e


async def load_api_data():
    """加载API数据"""
    logger.debug("开始加载API数据")
    try:
        await Api.create(
            method="get",
            path="/api/test",
            summary="测试API",
            tags=["system", "test"],
            status="1",
        )
        await Api.create(
            method="post",
            path="/api/test/create",
            summary="创建测试API",
            tags=["system", "create"],
            status="1",
        )
        await Api.create(
            method="delete",
            path="/api/test/delete",
            summary="删除测试API",
            tags=["system", "delete"],
            status="1",
        )
        logger.debug("API数据加载成功")
    except Exception as e:
        logger.error("加载API数据时发生异常: %s", e)
        raise e


async def load_menu_data():
    """加载菜单数据"""
    logger.debug("开始加载菜单数据")
    try:
        await Menu.create(
            menu_name="系统管理",
            menu_type="1",
            route_name="system",
            route_path="/system",
            i18n_key="menu.system",
            order=1,
            icon="settings",
            icon_type="1",
            status="1",
        )
        await Menu.create(
            menu_name="用户管理",
            menu_type="1",
            route_name="user",
            route_path="/user",
            i18n_key="menu.user",
            order=2,
            icon="user",
            icon_type="1",
            status="1",
        )
        await Menu.create(
            menu_name="角色管理",
            menu_type="1",
            route_name="role",
            route_path="/role",
            i18n_key="menu.role",
            order=3,
            icon="team",
            icon_type="2",
            status="1",
        )
        logger.debug("菜单数据加载成功")
    except Exception as e:
        logger.error("加载菜单数据时发生异常: %s", e)
        raise e


async def load_database_data():
    """加载数据库数据"""
    logger.debug("开始加载数据库数据")
    try:
        await Database.create(
            name="测试数据库",
            type="MySQL",
            host="localhost",
            port=3306,
            username="root",
            password="123456",
            database="test",
            status="1",
            update_by_id=1,
            create_by_id=1,
        )
        await Database.create(
            id=2,
            name="TestDB2",
            type="PostgreSQL",
            host="192.168.1.100",
            port=5432,
            username="admin",
            password="securepass",
            database="testdb2",
            status="0",
            description="测试数据库2",
            update_by_id=1,
            create_by_id=1,
        )
        logger.debug("数据库数据加载成功")
    except Exception as e:
        logger.error("加载数据库数据时发生异常: %s", e)
        raise e


async def load_model_data():
    """加载模型数据"""
    logger.debug("开始加载模型数据")
    try:
        await DataModel.create(
            name="用户模型",
            description="存储用户相关信息的模型",
            status="1",
            table_name="user_table",
            columns_conf='{"fields": [{"name": "id", "type": "int"}, {"name": "name", "type": "string"}]}',
            database_id=1,
            update_by_id=1,
            create_by_id=1,
        )
        await DataModel.create(
            name="订单模型",
            description="存储订单相关信息的模型",
            status="0",
            table_name="order_table",
            columns_conf='{"fields": [{"name": "order_id", "type": "int"}, {"name": "amount", "type": "float"}]}',
            database_id=1,
            update_by_id=1,
            create_by_id=1,
        )
        logger.debug("模型数据加载成功")
    except Exception as e:
        logger.error("加载模型数据时发生异常: %s", e)
        raise e


async def load_tag_data():
    """加载标签数据"""
    logger.debug("开始加载标签数据")
    try:
        await Tag.create(
            tag_name="测试模型",
            tag_type="模型类型",
            tag_desc="测试模型描述",
            update_by_id=1,
            create_by_id=1,
        )
        logger.debug("标签数据加载成功")
    except Exception as e:
        logger.error("加载标签数据时发生异常: %s", e)
        raise e


async def load_domain_data():
    """加载域数据"""
    logger.debug("开始加载域数据")
    try:
        await Domain.create(
            domain_name="测试数据域",
            domain_desc="测试数据域描述",
            domain_type="2",  # 1 表示数据域
            update_by_id=1,
            create_by_id=1,
        )
        await Domain.create(
            domain_name="测试主题域",
            domain_desc="测试主题域描述",
            domain_type="2",  # 2 表示主题域
            update_by_id=1,
            create_by_id=1,
        )
        logger.debug("域数据加载成功")
    except Exception as e:
        logger.error("加载域数据时发生异常: %s", e)
        raise e


async def load_metric_data():
    """加载指标数据"""
    logger.debug("开始加载指标数据")
    try:
        await Metric.create(
            metric_name="用户增长率",
            metric_desc="统计用户增长率的指标",
            statistical_period="monthly",
            statistic_scope=1000,
            chart_type="line",  # 对应 ChartType 枚举值
            sensitivity="high",  # 对应 Sensitivity 枚举值
            data_model_id=1,  # 假设关联的数据模型 ID 为 1
            create_by_id=1,  # 假设创建人 ID 为 1
        )

        await Metric.create(
            metric_name="订单完成率",
            metric_desc="统计订单完成率的指标",
            statistical_period="weekly",
            statistic_scope=500,
            chart_type="bar",  # 对应 ChartType 枚举值
            sensitivity="medium",  # 对应 Sensitivity 枚举值
            data_model_id=2,  # 假设关联的数据模型 ID 为 2
            create_by_id=2,  # 假设创建人 ID 为 2
        )
        logger.debug("指标数据加载成功")
    except Exception as e:
        logger.error("加载指标数据时发生异常: %s", e)
        raise e


async def load_test_data():
    """加载测试数据
    加载流程：
    系统：角色->用户->按钮->api->菜单
    资产：域->数据库->模型->标签->指标
    """
    # system
    await load_role_data()
    await load_user_data()
    await load_button_data()
    await load_api_data()
    await load_menu_data()

    # asset
    await load_domain_data()
    await load_database_data()
    await load_model_data()
    await load_tag_data()
    await load_metric_data()
