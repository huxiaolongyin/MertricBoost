import uvicorn

from metricboost.logger import LOGGING_CONFIG

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",  # 允许外部访问
        port=9999,
        reload=True,
        log_config=LOGGING_CONFIG,  # 日志配置
    )
