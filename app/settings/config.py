from pathlib import Path
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    VERSION: str = "0.1.0"
    APP_TITLE: str = "MetricBoost"
    PROJECT_NAME: str = "MetricBoost"
    APP_DESCRIPTION: str = "用于记录和分析各种指标和数据"

    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]

    ADD_LOG_ORIGINS_INCLUDE: list = [
        "*"
    ]  # APILoggerMiddleware and APILoggerAddResponseMiddleware
    ADD_LOG_ORIGINS_DECLUDE: list = [
        "/system-manage",
        "/redoc",
        "/doc",
        "/openapi.json",
    ]

    DEBUG: bool = True

    # 数据库设置
    # 加载env 文件
    load_dotenv()
    MYSQL_DB_HOST: str = os.environ.get("MYSQL_DB_HOST")
    MYSQL_DB_PORT: int = int(os.environ.get("MYSQL_DB_PORT"))
    MYSQL_DB_USER: str = os.environ.get("MYSQL_DB_USER")
    MYSQL_DB_PASSWORD: str = os.environ.get("MYSQL_DB_PASSWORD")
    MYSQL_DB_DATABASE: str = os.environ.get("MYSQL_DB_DATABASE")

    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
    BASE_DIR: Path = PROJECT_ROOT.parent
    LOGS_ROOT: Path = BASE_DIR / "app/logs"
    SECRET_KEY: str = (
        "ec2d7bedf5a0844ffd8142282fa4b912e8db973965ae625ebac55a08c4a60435"  # python -c "from passlib import pwd; print(pwd.genword(length=64, charset='hex'))"
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 12  # 12 hours
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    TORTOISE_ORM: dict = {
        "connections": {
            # If an error occurs, you can try to delete the "migrations/app_system" folder and all tables, and then run the project again
            # "conn_system": {
            #     "engine": "tortoise.backends.sqlite",
            #     "credentials": {"file_path": f"{BASE_DIR}/db_system.sqlite3"},
            # },
            # you need to create a database named `fast-soy-admin` in your database before running the project
            # if you want to use PostgreSQL, you need to install tortoise-orm[asyncpg]
            # "conn_system": {
            #     "engine": "tortoise.backends.asyncpg",
            #     "credentials": {
            #         "host": "localhost",
            #         "port": 5432,
            #         "user": "sleep1223",
            #         "password": "sleep1223",
            #         "database": "fast-soy-admin"
            #     }
            # },
            # if you want to use MySQL/MariaDB, you need to install tortoise-orm[asyncmy]
            "conn_system": {
                "engine": "tortoise.backends.mysql",
                "credentials": {
                    "host": MYSQL_DB_HOST,
                    "port": MYSQL_DB_PORT,
                    "user": MYSQL_DB_USER,
                    "password": MYSQL_DB_PASSWORD,
                    "database": MYSQL_DB_DATABASE,
                },
            },
            # if you want to use MSSQL/Oracle, you need to install tortoise-orm[asyncodbc]
            # "conn_book": {
            #     "engine": "tortoise.backends.asyncodbc",
            #     "credentials": {
            #         "host": "localhost",
            #         "port": 63306,
            #         "user": "sleep1223",
            #         "password": "sleep1223",
            #         "database": "fast-soy-admin"
            #     }
            # },
        },
        "apps": {
            # don't modify `app_system`, otherwise you will need to modify all `app_systems` in app/models/admin.py
            "app_system": {
                "models": [
                    "app.models.system",
                    "aerich.models",
                    "app.models.metric",
                ],
                "default_connection": "conn_system",
            },
            # "app_book": {"models": ["app.models.book"], "default_connection": "conn_book"},
        },
        "use_tz": False,
        "timezone": "Asia/Shanghai",
    }
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
