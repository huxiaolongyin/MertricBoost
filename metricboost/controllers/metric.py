from datetime import datetime

from cachetools import TTLCache
from tortoise.expressions import Q

from metricboost.core.crud import CRUDBase
from metricboost.logger import get_logger
from metricboost.models.asset import DataModel, Domain, Tag
from metricboost.models.enums import StatisticalPeriod
from metricboost.models.metric import Metric
from metricboost.schemas.metric import MetricCreate, MetricUpdate

logger = get_logger(__name__)


class MetricController(CRUDBase[Metric, MetricCreate, MetricUpdate]):
    _cache = TTLCache(maxsize=100, ttl=600)

    def __init__(self):
        super().__init__(model=Metric)

    async def create(self, obj_in: MetricCreate) -> Metric:
        """创建指标"""
        # 检查数据模型是否存在
        data_model = await DataModel.get_or_none(id=obj_in.data_model_id)
        if not data_model:
            raise ValueError("指定的数据模型不存在")

        # 准备指标数据，排除关联字段
        metric_data = obj_in.model_dump(
            exclude={"domain_ids", "tag_ids"}, exclude_unset=True
        )

        # 把data_model_id改名为data_model_id
        metric_data["data_model_id"] = metric_data.pop("data_model_id", None)

        # 创建指标
        metric = await super().create(metric_data)

        # 处理域关联
        # if hasattr(obj_in, "domain_ids") and obj_in.domain_ids:
        #     domains = await Domain.filter(id__in=obj_in.domain_ids)
        #     await metric.domains.add(*domains)

        # 处理标签关联
        if hasattr(obj_in, "tag_ids") and obj_in.tag_ids:
            tags = await Tag.filter(id__in=obj_in.tag_ids)
            await metric.tags.add(*tags)

        return metric

    async def update(self, id: int, obj_in: MetricUpdate) -> Metric:
        """更新指标"""
        metric = await self.get(id=id)
        if not metric:
            raise ValueError("指标不存在")

        # 检查数据模型是否存在
        if obj_in.data_model_id is not None:
            data_model = await DataModel.get_or_none(id=obj_in.data_model_id)
            if not data_model:
                raise ValueError("指定的数据模型不存在")

        # 准备指标数据，排除关联字段
        metric_data = obj_in.model_dump(
            exclude={"domain_ids", "tag_ids"}, exclude_unset=True
        )

        # 更新指标
        updated_metric = await super().update(id=id, obj_in=metric_data)

        # 处理域关联
        # if hasattr(obj_in, "domain_ids") and obj_in.domain_ids is not None:
        #     # 清除现有关联
        #     await updated_metric.domains.clear()
        #     # 添加新关联
        #     if obj_in.domain_ids:
        #         domains = await Domain.filter(id__in=obj_in.domain_ids)
        #         await updated_metric.domains.add(*domains)

        # 处理标签关联
        if hasattr(obj_in, "tag_ids") and obj_in.tag_ids is not None:
            # 清除现有关联
            await updated_metric.tags.clear()
            # 添加新关联
            if obj_in.tag_ids:
                tags = await Tag.filter(id__in=obj_in.tag_ids)
                await updated_metric.tags.add(*tags)

        return updated_metric

    async def _format_metric_to_dict(
        self,
        metric: Metric,
        date_range: list = None,
        statistical_period: str = None,
        dim_select: str = None,
        dim_filter: list[str] = None,
        sort: str = None,
        is_detail: bool = False,
    ) -> dict:
        """
        将指标对象格式化为字典

        Args:
            metric: 指标对象
            include_data: 是否包含指标数据
            date_range: 数据日期范围
            dim_select: 选择的维度列表
            dim_filter: 过滤条件

        Returns:
            格式化后的指标字典
        """
        await metric.data_model.fetch_related("domains")
        metric_dict = {
            "id": metric.id,
            "metricName": metric.metric_name,
            "statisticScope": metric.statistic_scope,
            "statisticalPeriod": metric.statistical_period,
            "metricDesc": metric.metric_desc,
            "chartType": metric.chart_type,
            "sensitivity": metric.sensitivity,
            "dataModelId": metric.data_model_id,
            "updateTime": metric.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "createTime": metric.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "updateBy": metric.update_by.user_name,
            "createBy": metric.create_by.user_name,
            "tags": [tag.tag_name for tag in metric.tags],
            "domains": [domain.domain_name for domain in metric.data_model.domains],
            "metricFormat": metric.data_model.metric_format,
            "dimCols": metric.data_model.dimension_columns,
            "data": await self.get_metric_data(
                metric.id,
                date_range,
                statistical_period or metric.statistical_period,
                dim_select,
                dim_filter,
                sort=sort,
            ),
        }
        if is_detail:
            metric_dict["dimData"] = await self.get_metric_dim_data(
                date_range, metric.data_model
            )

        return metric_dict

    async def get_metric_dim_data(self, date_range: list, data_model: DataModel):
        """
        获取指标的维度数据
        """
        _, date_where_clause, _ = self._build_date_condition(
            date_col=data_model.date_column,
            default_scope=30,
            date_range=date_range,
        )
        await data_model.fetch_related("database")
        if not data_model.dimension_columns:
            return []
        db = data_model.database

        # 拼接 SQL
        dim_data_list = []
        for dim_cols in data_model.dimension_columns:
            sql = f"""
            SELECT {dim_cols.get("value")} 
            FROM {data_model.table_name} 
            WHERE {date_where_clause}
            GROUP BY {dim_cols.get("value")} 
            """
            dim_data = await db.execute(sql)
            if not dim_data:
                return []
            dim_data_list.extend(dim_data)

        result = {}

        # 按键对所有值进行分组
        for item in dim_data_list:
            for key, value in item.items():
                if key not in result:
                    result[key] = []
                if value not in ["null", "NULL", None, "", "-99", "None"]:
                    result[key].append(value)

        # 转换为所需的输出格式
        return [{key: values} for key, values in result.items()]

    async def get_detail(
        self,
        id: int,
        date_range: list = None,
        statistical_period: str = None,
        dim_select: str = None,
        dim_filter: list[str] = None,
        sort: str = None,
    ):
        """
        获取单个指标的详细信息和数据

        Args:
            id: 指标ID
            dim_select: 选择的维度列表
            date_range: 数据日期范围
            dim_filter: 过滤条件
            order: 排序方式

        Returns:
            单个指标的详细信息和数据
        """
        metric: Metric = await super().get(id)
        if not metric:
            return None

        # 加载关联数据
        await metric.fetch_related("tags", "create_by", "update_by", "data_model")

        return await self._format_metric_to_dict(
            metric,
            date_range=date_range,
            statistical_period=statistical_period,
            dim_select=dim_select,
            dim_filter=dim_filter,
            sort=sort,
            is_detail=True,
        )

    async def get_list(
        self,
        page: int = 1,
        page_size: int = 10,
        search: Q = Q(),
        order: str = None,
        distinct: bool = False,
    ):
        """
        获取指标列表

        Args:
            page: 页码
            page_size: 每页数量
            search: 查询条件
            order: 排序方式

        Returns:
            total, metrics: 总数和指标列表
        """
        total, metric_list = await super().get_list(
            page=page,
            page_size=page_size,
            search=search,
            order=order,
            prefetch=["tags", "create_by", "update_by", "data_model"],
            distinct=distinct,
        )

        result = []
        for metric in metric_list:
            metric_dict = await self._format_metric_to_dict(metric)
            result.append(metric_dict)

        return total, result

    async def get_metric_data(
        self,
        metric_id: int,
        date_range: list = None,
        statistical_period: str = None,
        dim_select: str = None,
        dim_filter: list[str] = None,
        sort: str = None,
    ):
        """获取指标数据

        Args:
            metric_id: 指标ID
            date_range: 数据日期范围 [开始日期, 结束日期]
            statistical_period: 统计周期
            dim_select: 选择的维度列表
            dim_filter: 过滤条件

        Returns:
            list[dict]: 查询结果，如果指标为空则返回最近周期的数值为{'date':0}的列表
            例如 metric.statistical_period == StatisticalPeriod.daily

        Raises:
            ValueError: 当指标不存在或查询失败时
        """
        if sort not in ["ASC", "DESC"]:
            sort = "DESC"
        # 获取指标和数据模型
        metric = await self.get(id=metric_id)
        if not metric:
            raise ValueError("指标不存在")

        data_model = await DataModel.get(id=metric.data_model_id).prefetch_related(
            "database"
        )
        if not data_model:
            raise ValueError("数据模型不存在")

        # 提取配置信息
        default_scope = metric.statistic_scope
        db = data_model.database
        table = data_model.table_name
        date_col = data_model.date_column
        metric_col = data_model.metric_column
        agg = data_model.agg_method
        extra_calc = data_model.extra_caculate

        # 构建日期条件
        date_format_sql, date_where_clause, date_list = self._build_date_condition(
            date_col, default_scope, date_range, statistical_period
        )

        # 处理维度字段
        dim_clause = self._prepare_dimension_clauses(dim_select)

        # 处理维度过滤条件
        dim_where_clause = self._build_dim_filter_clause(dim_filter)

        # 构建SQL查询
        if statistical_period != "cumulative":
            if dim_select:
                # 如果有维度选择，则使用窗口函数限制每个日期的前15条记录
                sql = f"""
                WITH ranked_data AS (
                    SELECT
                        {date_format_sql} as date,
                        {agg}({metric_col}){extra_calc} as value{dim_clause},
                        ROW_NUMBER() OVER (PARTITION BY {date_format_sql} ORDER BY {agg}({metric_col}){extra_calc} {sort}) as row_num
                    FROM {table}
                    WHERE {date_where_clause}{dim_where_clause}
                    GROUP BY {date_format_sql}{dim_clause}
                )
                SELECT date, value{dim_clause} 
                FROM ranked_data
                WHERE row_num <= 10
                ORDER BY date, value {sort}
                """
            else:
                # 原始查询，不限制记录数
                sql = f"""
                SELECT
                    {date_format_sql} as date,
                    {agg}({metric_col}){extra_calc} as value{dim_clause}
                FROM {table}
                WHERE {date_where_clause}{dim_where_clause}
                GROUP BY {date_format_sql}{dim_clause}
                ORDER BY date, value DESC
                """
        else:
            sql = f"""
            SELECT
                current_date() as date,
                {agg}({metric_col}){extra_calc} as value{dim_clause}
            FROM {table}
            WHERE {date_where_clause}{dim_where_clause}
            ORDER BY date, value DESC
            """
        result = await db.execute(sql)

        try:
            return result or [{"date": date, "value": 0} for date in date_list]
        except Exception as e:
            logger.error(f"查询执行错误: {str(e)}")
            raise ValueError(f"数据查询失败: {str(e)}")

    def _build_date_condition(
        self,
        date_col: str,
        default_scope: int,
        date_range: list[datetime] = None,
        statistical_period: StatisticalPeriod = None,
    ):
        """构建日期条件子句和日期列表

        Args:
            metric: 指标对象
            date_range: 日期范围
            statistical_period: 统计周期

        Returns:
            date_format_sql: 时间格式化子句，通过DATE_FORMAT + statistical_period 比较格式化日期
            date_where_clause: 日期条件子句，用于指定日期范围
            date_list: 日期列表，包含符合条件的日期

        """
        logger.debug(
            f"构建日期条件: {date_col}, {default_scope}, {date_range}, {statistical_period}"
        )
        try:
            from datetime import datetime, timedelta

            from dateutil.relativedelta import relativedelta

            today = datetime.now().date()

            # 定义特定于期间的设置
            period_settings = {
                "daily": {
                    "format": "%Y-%m-%d",
                    "date_func": lambda dt: dt.strftime("%Y-%m-%d"),
                    "increment": lambda dt, i: dt + timedelta(days=i),
                    "default_start": lambda: today - timedelta(days=default_scope),
                    "sql_format": f"DATE_FORMAT({date_col}, '%Y-%m-%d')",
                },
                "weekly": {
                    "format": "%Y-%U",  # Year-WeekNumber
                    "date_func": lambda dt: dt.strftime("%Y-%U"),  # Format as "YYYY-WW"
                    "increment": lambda dt, i: dt + timedelta(weeks=i),
                    "default_start": lambda: today - timedelta(weeks=default_scope),
                    "sql_format": f"DATE_FORMAT({date_col}, '%Y-%U')",
                },
                "monthly": {
                    "format": "%Y-%m",
                    "date_func": lambda dt: dt.strftime("%Y-%m"),  # Format as "YYYY-MM"
                    "increment": lambda dt, i: dt + relativedelta(months=i),
                    "default_start": lambda: (
                        today - relativedelta(months=default_scope)
                    ).replace(day=1),
                    "sql_format": f"DATE_FORMAT({date_col}, '%Y-%m')",
                },
                "yearly": {
                    "format": "%Y",
                    "date_func": lambda dt: dt.strftime("%Y"),  # Format as "YYYY"
                    "increment": lambda dt, i: dt + relativedelta(years=i),
                    "default_start": lambda: (
                        today - relativedelta(years=default_scope)
                    ).replace(month=1, day=1),
                    "sql_format": f"DATE_FORMAT({date_col}, '%Y')",
                },
                "cumulative": {
                    "format": "%Y-%m-%d",
                    "date_func": lambda dt: dt.strftime("%Y-%m-%d"),
                    "increment": lambda dt, i: dt + timedelta(days=i),
                    "default_start": lambda: today - timedelta(days=default_scope),
                    "sql_format": f"DATE_FORMAT({date_col}, '%Y-%m-%d')",
                },
            }

            # 获取统计周期对应的设置
            settings = period_settings.get(statistical_period, period_settings["daily"])

            # Step 1: 生成维度SQL子句
            date_format_sql = settings["sql_format"]

            # Step 2: 判断是否是累计
            if statistical_period == "cumulative":
                date_where_clause = "1=1"  # 始终为真的条件，不过滤时间

                # 对于累计，我们只需要返回最近的一个日期
                end_date = today
                date_list = [today.strftime(settings["format"])]
            else:
                # Step 2: 生成 MySQL 筛选条件
                # 如果传入了日期范围，则使用传入的日期范围
                if date_range and len(date_range) == 2:
                    start_date = datetime.strptime(date_range[0], "%Y-%m-%d").date()
                    end_date = datetime.strptime(date_range[1], "%Y-%m-%d").date()
                    date_where_clause = (
                        f"{date_col} BETWEEN '{date_range[0]}' AND '{date_range[1]}'"
                    )

                # 如果没有传入日期范围，则使用默认的日期范围
                else:
                    start_date = settings["default_start"]()
                    end_date = today
                    date_where_clause = (
                        f"{date_col} >= '{start_date.strftime('%Y-%m-%d')}'"
                    )

                # Step 3: 生成日期序列
                date_list = []
                current_date = start_date

                if statistical_period == "weekly":
                    # Start from the first day of the week containing start_date
                    current_date = current_date - timedelta(days=current_date.weekday())
                elif statistical_period == "monthly":
                    # Start from the first day of the month
                    current_date = current_date.replace(day=1)
                elif statistical_period == "yearly":
                    # Start from the first day of the year
                    current_date = current_date.replace(month=1, day=1)

                # Track already added periods to avoid duplicates
                added_periods = set()

                # Generate the sequence
                while current_date <= end_date:
                    period_str = settings["date_func"](current_date)

                    # Only add if we haven't added this period yet
                    if period_str not in added_periods:
                        date_list.append(period_str)
                        added_periods.add(period_str)

                        current_date = settings["increment"](current_date, 1)
            logger.debug(
                f"日期格式化SQL: {date_format_sql}, 日期条件: {date_where_clause},  日期列表: {date_list}"
            )

            return date_format_sql, date_where_clause, date_list
        except Exception as e:
            logger.error(f"生成日期序列失败: {e}")
            raise

    def _prepare_dimension_clauses(self, dim_select: str = None):
        """准备维度相关的SQL子句"""
        if not dim_select or not dim_select[0]:
            return ""

        logger.debug(f"准备维度条件: {dim_select}")
        try:
            result = ", " + dim_select
            logger.debug(f"准备维度条件成功: {result}")
            return result
        except Exception as e:
            logger.error(f"准备维度条件失败: {e}")
            raise

    def _build_dim_filter_clause(self, dim_filter: list[str]):
        """构建维度过滤条件"""
        if not dim_filter or dim_filter[0] == "":
            return ""

        return "AND " + " AND ".join(dim_filter)

    async def add_tag(self, metric_id: int, tag_id: int):
        """添加指标标签"""
        # 检查指标是否存在
        metric = await Metric.get_or_none(id=metric_id)
        if not metric:
            raise ValueError("指标不存在")

        # 检查标签是否存在
        tag = await Tag.get_or_none(id=tag_id)
        if not tag:
            raise ValueError(msg="标签不存在")

        # 添加标签
        await metric.tags.add(tag)

        return metric

    async def remove_tag(self, metric_id: int, tag_name: str):
        """移除指标标签"""
        # 检查指标是否存在
        metric = await Metric.get_or_none(id=metric_id)
        if not metric:
            raise ValueError("指标不存在")

        # 检查标签是否存在
        tag = await Tag.get_or_none(tag_name=tag_name)
        if not tag:
            raise ValueError(msg="标签不存在")

        # 移除标签
        await metric.tags.remove(tag)

        return metric


metric_controller = MetricController()
