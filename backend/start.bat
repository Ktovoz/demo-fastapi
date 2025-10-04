@echo off
echo 🚀 启动 FastAPI 后端服务...
echo.

REM 检查虚拟环境是否存在
if not exist "venv\Scripts\activate.bat" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 📥 安装依赖包...
pip install -r requirements.txt

REM 复制环境变量文件（如果不存在）
if not exist ".env" (
    echo 📝 创建环境变量文件...
    copy .env.example .env
)

REM 启动服务器
echo 🚀 启动服务器...
python run.py

pause