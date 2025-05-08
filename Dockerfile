FROM python:3.11-slim

WORKDIR /code

# 复制源代码
COPY ./metricboost ./metricboost
COPY ./pyproject.toml  .
COPY ./README.md .

USER root

# Install UV
RUN pip3 install uv 

# 配置pip并安装依赖
RUN uv pip install --system --no-cache-dir .

# 暴露端口
EXPOSE 9999

CMD ["python","/code/metricboost/main.py"]