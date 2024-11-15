import json
from app.core.crud import CRUDBase
from app.models.system import DataModel, User, TopicDomain, DataDomain, Database
from app.schemas.data_model import DataModelCreate, DataModelUpdate
from tortoise import Tortoise


class DataModelController(CRUDBase[DataModel, DataModelCreate, DataModelUpdate]):
    def __init__(self):
        super().__init__(model=DataModel)

    async def get_by_status(self, status: str) -> DataModel | None:
        return await self.model.filter(status=status).first()

    async def get_by_creator(self, creator: str) -> DataModel | None:
        return await self.model.filter(creator=creator).first()

    async def create(self, obj_in: DataModelCreate) -> DataModel:
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        obj_in.database = await Database.get(id=obj_in.database)
        obj_in.data_domain = await DataDomain.get(id=obj_in.data_domain)
        obj_in.topic_domain = await TopicDomain.get(id=obj_in.topic_domain)
        return await super().create(obj_in)

    async def update(self, id: int, obj_in: DataModelUpdate) -> DataModel:  # type: ignore
        obj_in.create_by = await User.get(user_name=obj_in.create_by)
        obj_in.database = await Database.get(id=obj_in.database)
        obj_in.data_domain = await DataDomain.get(id=obj_in.data_domain)
        obj_in.topic_domain = await TopicDomain.get(id=obj_in.topic_domain)
        return await super().update(id=id, obj_in=obj_in)

    async def remove(self, id: int) -> DataModel:
        return await super().remove(id=id)

    async def sql_preview(self, database_id: int, sql_content: str):
        """通过保存的数据库链接，和sql内容，返回预览数据"""
        database = await Database.get(id=database_id)
        if database:
            connection_url = f"mysql://{database.database_user}:{database.password}@{database.database_host}:{database.database_port}/{database.database_database}"
            await Tortoise.init(
                db_url=connection_url, modules={"models": []}, timezone="Asia/Shanghai"
            )

            #  生成在Tortoise ORM模型中定义的数据库模式。
            #  此方法通常在应用程序初始化期间调用，以确保数据库模式与已定义的模型保持一致。它将根据模型定义在数据库中创建任何缺失的表或列。
            # await Tortoise.generate_schemas()

            # 设置来自 Tortoise ORM 的默认数据库连接。
            conn = Tortoise.get_connection(connection_name="default")

            try:
                # 执行 SQL 查询
                total, results = await conn.execute_query(sql_content)

                # 获取列名
                columns = list(results[0].keys())
                return total, columns, results

            except Exception as e:
                print(f"执行 SQL 查询时出错: {e}")
                return []  # 返回空列表或处理错误

            finally:
                # 关闭数据库连接
                await Tortoise.close_connections()

    async def fetch_tables_metadata(self, database_id: int):
        """获取表的元数据信息"""
        database = await Database.get(id=database_id)
        if database and database.database_type.lower() == "mysql":
            connection_url = f"mysql://{database.database_user}:{database.password}@{database.database_host}:{database.database_port}/{database.database_database}"
            await Tortoise.init(
                db_url=connection_url, modules={"models": []}, timezone="Asia/Shanghai"
            )
            sql_query = f"""
                SELECT
                    TABLE_NAME,
                    TABLE_COMMENT
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = '{database.database_database}'
            """
            conn = Tortoise.get_connection(connection_name="default")
            try:
                # 执行 SQL 查询
                total, results = await conn.execute_query(sql_query)
                return total, results

            except Exception as e:
                print(f"执行 SQL 查询时出错: {e}")
                return 0, []  # 返回空列表或处理错误

            finally:
                # 关闭数据库连接
                await Tortoise.close_connections()

    async def fetch_columns_metadata(self, database_id: int, table_name: str):
        """获取字段的元数据"""
        database = await Database.get(id=database_id)
        if database and database.database_type.lower() == "mysql":
            connection_url = f"mysql://{database.database_user}:{database.password}@{database.database_host}:{database.database_port}/{database.database_database}"
        else:
            return 0, "暂不支持其他数据库"

        await Tortoise.init(
            db_url=connection_url, modules={"models": []}, timezone="Asia/Shanghai"
        )

        sql_query = f"""
            SELECT 
                COLUMN_NAME as columnName, 
                COLUMN_TYPE as columnType, 
                COLUMN_COMMENT as columnComment,
                NULL as semanticType,
                NULL as format,
                NULL as staticType
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = '{database.database_database}'
            AND TABLE_NAME = '{table_name}'
        """
        conn = Tortoise.get_connection(connection_name="default")
        try:
            total, results = await conn.execute_query(sql_query)

            # 获取数据模型配置
            datamodel = await DataModel.filter(
                database_id=database_id, table_name=table_name
            ).first()

            if not datamodel:
                return total, results
            # 解析字段配置
            try:
                field_conf = json.loads(datamodel.field_conf)
            except:
                print("field_conf 解析失败")
                return total, results

            if not field_conf:
                return total, results

            # 创建字段配置映射，提高查找效率
            field_map = {d["columnName"]: d for d in field_conf}

            # 更新结果
            results = [
                {
                    **row,
                    **{
                        k: v
                        for k, v in field_map.get(row["columnName"], {}).items()
                        if k in row
                    },
                }
                for row in results
            ]

            return total, results

        except Exception as e:
            print(f"执行 SQL 查询时出错: {e}")
            return 0, []  # 返回空列表或处理错误

        finally:
            # 关闭数据库连接
            await Tortoise.close_connections()

    async def fetch_table_data(self, database_id: int, table_name: str):
        """获取数据表的数据"""
        database = await Database.get(id=database_id)
        if database and database.database_type.lower() == "mysql":
            connection_url = f"mysql://{database.database_user}:{database.password}@{database.database_host}:{database.database_port}/{database.database_database}"
            await Tortoise.init(
                db_url=connection_url, modules={"models": []}, timezone="Asia/Shanghai"
            )
            sql_query = f"""
                SELECT 
                    *
                FROM {table_name}
                LIMIT 200
            """
            conn = Tortoise.get_connection(connection_name="default")
            try:
                # 执行 SQL 查询
                total, results = await conn.execute_query(sql_query)
                return total, results
            except Exception as e:
                print(f"执行 SQL 查询时出错: {e}")
                return 0, []  # 返回空列表或处理错误
            finally:
                # 关闭数据库连接
                await Tortoise.close_connections()

    async def fetch_aggregate_data(
        self,
        data_model_id: str,
        statistic_column: str = None,
        statistic_type: str = None,
        aggregated_column: str = None,
    ):
        """从数据表中获取聚合的数据"""
        data_model = await DataModel.get_or_none(id=data_model_id)
        if data_model:
            # 统计字段
            statistic_column = (
                data_model.statistic_column
                if not statistic_column
                else statistic_column
            )
            # 统计方式
            statistic_type = (
                data_model.statistic_type if not statistic_type else statistic_type
            )
            # 聚合字段
            aggregated_column = (
                data_model.aggregated_column
                if not aggregated_column
                else aggregated_column
            )
            database_id = data_model.database_id
            database = await Database.get(id=database_id)
            if database and database.database_type.lower() == "mysql":
                connection_url = f"mysql://{database.database_user}:{database.password}@{database.database_host}:{database.database_port}/{database.database_database}"
                await Tortoise.init(
                    db_url=connection_url,
                    modules={"models": []},
                    timezone="Asia/Shanghai",
                )
                sql_query = f"""
                    SELECT
                        {aggregated_column},
                        {statistic_type}({statistic_column})
                    FROM {data_model.table_name}
                    GROUP BY {aggregated_column}
                """
                conn = Tortoise.get_connection(connection_name="default")
                try:
                    # 执行 SQL 查询
                    total, results = await conn.execute_query(sql_query)
                    return total, results
                except Exception as e:
                    print(f"执行 SQL 查询时出错: {e}")
                    return 0, []  # 返回空列表或处理错误
                finally:
                    # 关闭数据库连接
                    await Tortoise.close_connections()


data_model_controller = DataModelController()
