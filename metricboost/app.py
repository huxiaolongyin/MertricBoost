import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from metricboost.api.routers import router as api_router
from metricboost.core.exceptions import SettingNotFound
from metricboost.core.init_app import modify_db
from metricboost.core.middlewares import (
    APILoggerAddResponseMiddleware,
    APILoggerMiddleware,
    BackGroundTaskMiddleware,
)
from metricboost.load_test_data import load_test_data
from metricboost.logger import logger
from metricboost.models.system import Log, LogDetailType, LogType

try:
    from metricboost.config import SETTINGS
except ImportError:
    raise SettingNotFound("Can not import settings")


def create_app(config=None) -> FastAPI:
    app = FastAPI(
        title=SETTINGS.APP_TITLE,
        description=SETTINGS.APP_DESCRIPTION,
        version=SETTINGS.VERSION,
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        middleware=(
            Middleware(
                CORSMiddleware,
                allow_origins=SETTINGS.CORS_ORIGINS,
                allow_credentials=SETTINGS.CORS_ALLOW_CREDENTIALS,
                allow_methods=SETTINGS.CORS_ALLOW_METHODS,
                allow_headers=SETTINGS.CORS_ALLOW_HEADERS,
            ),
            Middleware(BackGroundTaskMiddleware),
            Middleware(APILoggerMiddleware),
            Middleware(APILoggerAddResponseMiddleware),
        ),
        # lifespan=lifespan,
    )
    # 将配置存储在应用状态中
    app.state.db_config = config

    app.router.lifespan_context = lifespan
    app.include_router(api_router, prefix="/api")
    # register_db(app)
    # register_exceptions(app)
    # register_routers(app, prefix="/api")
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理

    处理应用启动和关闭时的操作
    """
    start_time = time.time()
    # 初始化数据库连接
    config = app.state.db_config

    try:
        await modify_db(config)
        if config:
            await load_test_data()
        # await init_menus()
        # await refresh_api_list()
        # await init_users()
        await Log.create(
            log_type=LogType.SystemLog, log_detail_type=LogDetailType.SystemStart
        )
        yield
    finally:
        end_time = time.time()
        runtime = end_time - start_time
        print("")
        logger.info(f"应用 {app.title} 运行时间: {runtime:.2f} 秒")
        await Log.create(
            log_type=LogType.SystemLog, log_detail_type=LogDetailType.SystemStop
        )


app = create_app()
