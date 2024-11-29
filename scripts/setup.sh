#!/bin/bash

# 获取脚本所在目录
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# 启动后端
echo "启动后端..."
cd "$BASE_DIR/backend"

if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python -m venv venv
fi

source venv/bin/activate

pip install -r requirements.txt

# 使用 uvicorn 启动后端，启用热重载
uvicorn app.main:app --reload &
BACKEND_PID=$!

# 启动前端
echo "启动前端..."
cd "$BASE_DIR/frontend"

pnpm install
pnpm dev &
FRONTEND_PID=$!

# 捕获 Ctrl+C 信号
trap 'kill $BACKEND_PID; kill $FRONTEND_PID; exit' INT

# 保持脚本运行
wait