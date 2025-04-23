from pathlib import Path
from typing import Any, Dict

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 应用基本信息
    VERSION: str = "0.1.0"
    APP_TITLE: str = "MetricBoost"
    PROJECT_NAME: str = "MetricBoost"
    APP_DESCRIPTION: str = "用于记录和分析各种指标和数据"

    # CORS设置
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]

    # 日志设置
    ADD_LOG_ORIGINS_INCLUDE: list = [
        "*"
    ]  # APILoggerMiddleware and APILoggerAddResponseMiddleware
    ADD_LOG_ORIGINS_DECLUDE: list = [
        "/system-manage",
        "/redoc",
        "/doc",
        "/openapi.json",
    ]

    # 开发模式设置
    DEBUG: bool = True

    # 数据库设置 - 从环境变量获取
    MYSQL_DB_HOST: str
    MYSQL_DB_PORT: int
    MYSQL_DB_USER: str
    MYSQL_DB_PASSWORD: str
    MYSQL_DB_DATABASE: str

    # 路径设置
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent
    LOGS_DIR: Path = ROOT_DIR / "logs"

    # 安全设置
    SECRET_KEY: str = "ec2d7bedf5a0844ffd8142282fa4b912e8db973965ae625ebac55a08c4a60435"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 12  # 12 hours
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # 日期时间格式
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    # Tortoise ORM配置
    @property
    def TORTOISE_ORM(self) -> Dict[str, Any]:
        return {
            "connections": {
                "conn_system": {
                    "engine": "tortoise.backends.mysql",
                    "credentials": {
                        "host": self.MYSQL_DB_HOST,
                        "port": self.MYSQL_DB_PORT,
                        "user": self.MYSQL_DB_USER,
                        "password": self.MYSQL_DB_PASSWORD,
                        "database": self.MYSQL_DB_DATABASE,
                        "minsize": 1,
                        "maxsize": 100,
                    },
                },
            },
            "apps": {
                "app_system": {
                    "models": [
                        "aerich.models",
                        "metricboost.models.system",
                        "metricboost.models.asset",
                        "metricboost.models.metric",
                    ],
                    "default_connection": "conn_system",
                },
            },
            "use_tz": False,
            "timezone": "Asia/Shanghai",
        }

    # 配置Pydantic以使用.env文件
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


SETTINGS = Settings()
