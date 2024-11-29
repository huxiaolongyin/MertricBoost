@echo off
@REM 设置控制台代码页为 UTF-8
chcp 65001
@REM 设置控制台字体为 Consolas，支持中文显示
REG ADD "HKEY_CURRENT_USER\Console" /v "FaceName" /t REG_SZ /d "Consolas" /f

@REM 获取脚本所在目录的父目录
SET BASE_DIR=%~dp0..
SET BACKEND_DIR=%BASE_DIR%\backend
SET FRONTEND_DIR=%BASE_DIR%\frontend

@REM 启动后端
echo 启动后端...
cd /d "%BACKEND_DIR%"

IF NOT EXIST ".venv\Scripts\activate" (
    echo 创建虚拟环境...
    python -m venv .venv
)

echo 激活虚拟环境...
CALL .venv\Scripts\activate

@REM pip install -r requirements.txt

REM 使用 uvicorn 启动后端，启用热重载，在新窗口中运行
start "Backend" cmd /k python ./main.py

REM 启动前端
echo 启动前端...
cd /d "%FRONTEND_DIR%"

@REM pnpm install
@REM 在新窗口中运行前端开发服务器
start "Frontend" cmd /k pnpm dev

echo 请按任意键退出...
pause >nul

@REM 确保当前窗口也关闭
exit