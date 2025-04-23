import atexit
import logging
import os
import sys
from functools import lru_cache
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Any, Dict, Optional

from metricboost.config import SETTINGS
from metricboost.core.ctx import CTX_USER_ID
from metricboost.models.system import Api, Log, LogDetailType, LogType


class UvicornStyleFormatter(logging.Formatter):
    """模拟 uvicorn 日志格式的格式化器"""

    def __init__(self, use_colors: bool = False):
        """
        初始化格式化器

        Args:
            use_colors: 是否使用彩色输出
        """
        # uvicorn 格式: 2025-04-08 11:32:56,376 - uvicorn.error - INFO:     Waiting for application startup.
        fmt = "%(asctime)s - %(name)s - %(levelname)s:     %(message)s"
        self.use_colors = use_colors and sys.stdout.isatty()
        super().__init__(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")

    def formatTime(self, record, datefmt=None):
        """重写时间格式以匹配 uvicorn 的格式（带毫秒）"""
        # 先使用基类的格式化时间
        formatted_time = super().formatTime(record, datefmt)
        # 添加毫秒
        return f"{formatted_time},{record.msecs:03.0f}"

    def format(self, record):
        """格式化日志记录"""
        # 为消息添加前导空格，模拟 uvicorn 格式
        record.message = record.getMessage()
        record.message = "    " + record.message

        # 应用颜色（如果启用）
        if self.use_colors:
            colors = {
                "DEBUG": "\033[94m",  # 蓝色
                "INFO": "\033[92m",  # 绿色
                "WARNING": "\033[93m",  # 黄色
                "ERROR": "\033[91m",  # 红色
                "CRITICAL": "\033[91m\033[1m",  # 红色加粗
                "RESET": "\033[0m",
            }

            formatted_message = super().format(record)
            if record.levelname in colors:
                return f"{colors[record.levelname]}{formatted_message}{colors['RESET']}"
            return formatted_message
        else:
            return super().format(record)


class AppLogger:
    """应用程序日志管理类（uvicorn 风格）"""

    def __init__(
        self,
        name: str = "app",
        log_dir: Optional[str] = None,
        console_level: Optional[str] = None,
        file_level: Optional[str] = None,
        rotation_type: str = "size",
        use_colors: bool = True,
    ) -> None:
        """
        初始化日志管理器

        Args:
            name: 日志器名称
            log_dir: 日志存储目录，默认使用配置中的目录
            console_level: 控制台日志级别，默认使用配置中的级别
            file_level: 文件日志级别，默认使用配置中的级别
            rotation_type: 日志轮转类型，"size"按大小轮转，"time"按时间轮转
            use_colors: 是否在控制台使用彩色输出
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.log_dir = log_dir or getattr(SETTINGS, "LOGS_DIR", "logs")
        self.console_level = console_level or ("DEBUG" if SETTINGS.DEBUG else "INFO")
        self.file_level = file_level or ("DEBUG" if SETTINGS.DEBUG else "INFO")
        self.rotation_type = rotation_type
        self.use_colors = use_colors
        self.handlers = []

        # 确保日志目录存在
        os.makedirs(self.log_dir, exist_ok=True)

    def setup_logger(self) -> logging.Logger:
        """
        配置并返回日志记录器

        Returns:
            logging.Logger: 配置好的日志记录器
        """
        # 清除已有的处理器
        if self.logger.handlers:
            for handler in self.logger.handlers[:]:
                handler.close()
                self.logger.removeHandler(handler)

        # 设置日志级别为最低级别
        self.logger.setLevel(logging.DEBUG)

        # 添加控制台处理器
        self._add_console_handler()

        # 添加文件处理器
        self._add_file_handler()

        # 添加错误文件处理器
        self._add_error_file_handler()

        # 防止日志传播到根记录器
        self.logger.propagate = False

        # 注册退出时关闭所有处理器
        atexit.register(self._close_handlers)

        return self.logger

    def _add_console_handler(self) -> None:
        """添加控制台日志处理器"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, self.console_level))

        # 使用 uvicorn 风格格式化器（带颜色）
        console_formatter = UvicornStyleFormatter(use_colors=self.use_colors)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        self.handlers.append(console_handler)

    def _add_file_handler(self) -> None:
        """添加文件日志处理器"""
        log_file = os.path.join(self.log_dir, f"{self.name}.log")

        if self.rotation_type == "time":
            # 按时间轮转（每天一个日志文件）
            file_handler = TimedRotatingFileHandler(
                filename=log_file,
                when="midnight",
                interval=1,
                backupCount=30,  # 保留30天
                encoding="utf-8",
            )
        else:
            # 按大小轮转
            file_handler = RotatingFileHandler(
                filename=log_file,
                maxBytes=100 * 1024 * 1024,  # 100 MB
                backupCount=10,  # 保留10个备份文件
                encoding="utf-8",
            )

        file_handler.setLevel(getattr(logging, self.file_level))

        # 使用 uvicorn 风格格式化器（无颜色）
        file_formatter = UvicornStyleFormatter(use_colors=False)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        self.handlers.append(file_handler)

    def _add_error_file_handler(self) -> None:
        """添加错误日志文件处理器（仅ERROR及以上级别）"""
        error_log_file = os.path.join(self.log_dir, f"{self.name}_error.log")

        error_file_handler = RotatingFileHandler(
            filename=error_log_file,
            maxBytes=50 * 1024 * 1024,  # 50 MB
            backupCount=10,
            encoding="utf-8",
        )
        error_file_handler.setLevel(logging.ERROR)

        # 使用 uvicorn 风格格式化器（无颜色）
        error_formatter = UvicornStyleFormatter(use_colors=False)
        error_file_handler.setFormatter(error_formatter)
        self.logger.addHandler(error_file_handler)
        self.handlers.append(error_file_handler)

    def _close_handlers(self) -> None:
        """关闭所有日志处理器"""
        for handler in self.handlers:
            try:
                handler.close()
            except:
                pass


# 配置Uvicorn的日志处理
LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s - %(name)s - %(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(asctime)s - %(name)s - %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
        "access_file": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(asctime)s - %(name)s - %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
            "use_colors": False,
        },
    },
    "handlers": {
        "file_handler": {
            "formatter": "access_file",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"{SETTINGS.LOGS_DIR}/uvicorn_access.log",
            "mode": "a+",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {
            "handlers": ["access", "file_handler"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


@lru_cache(maxsize=32)
def get_logger(
    name: str = "app",
    log_dir: Optional[str] = None,
    console_level: Optional[str] = None,
    file_level: Optional[str] = None,
    rotation_type: str = "size",
    use_colors: bool = True,
) -> logging.Logger:
    """
    获取指定名称的日志记录器（带缓存）

    Args:
        name: 日志记录器名称
        log_dir: 日志文件存储目录
        console_level: 控制台日志级别
        file_level: 文件日志级别
        rotation_type: 日志轮转类型
        use_colors: 是否使用彩色输出

    Returns:
        配置好的日志记录器
    """
    logger_instance = AppLogger(
        name=name,
        log_dir=log_dir,
        console_level=console_level,
        file_level=file_level,
        rotation_type=rotation_type,
        use_colors=use_colors,
    )
    return logger_instance.setup_logger()


async def insert_log(
    log_type: LogType,
    log_detail_type: LogDetailType,
    log_detail: str | None = None,
    by_user_id: int | None = None,
):
    """
    插入日志
    Args:
        log_type: 日志类型
        log_detail_type: 日志详情类型
        log_detail: 日志详情
        by_user_id: 0为从上下文获取当前用户id, 需要请求携带token
    :return:
    """
    if by_user_id == 0 and (by_user_id := CTX_USER_ID.get()) == 0:
        by_user_id = None

    await Log.create(
        log_type=log_type,
        log_detail_type=log_detail_type,
        log_detail=log_detail,
        by_user_id=by_user_id,
    )


# 创建默认日志实例
logger = get_logger("metricboost")
