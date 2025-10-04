from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import time
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# 导入日志系统
from app.utils.logger import app_logger, get_logger

# 加载环境变量
load_dotenv()

# 获取日志记录器
logger = get_logger(__name__)

# 导入路由
try:
    from app.routers import api
except ImportError:
    from routers import api

# 应用生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    logger.info("🚀 FastAPI 应用正在启动...")
    logger.info(f"📋 应用名称: {os.getenv('APP_NAME', 'Demo FastAPI')}")
    logger.info(f"🔧 版本: {os.getenv('APP_VERSION', '1.0.0')}")
    logger.info(f"🔍 调试模式: {os.getenv('DEBUG', 'False')}")

    yield

    # 关闭时执行
    logger.info("🛑 FastAPI 应用正在关闭...")

# 创建 FastAPI 应用实例
app = FastAPI(
    title=os.getenv("APP_NAME", "Demo FastAPI"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="一个前后端分离的示例项目",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # 允许的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # 记录请求信息
    client_ip = request.client.host
    method = request.method
    url = str(request.url)
    user_agent = request.headers.get("user-agent", "Unknown")

    logger.info(f"📥 请求开始: {method} {url} | 客户端: {client_ip} | User-Agent: {user_agent}")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        status_code = response.status_code

        # 记录响应信息
        logger.info(f"📤 请求完成: {method} {url} | 状态码: {status_code} | 耗时: {process_time:.3f}s")

        # 添加响应头
        response.headers["X-Process-Time"] = str(process_time)

        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"❌ 请求失败: {method} {url} | 错误: {str(e)} | 耗时: {process_time:.3f}s")
        raise

# 包含路由
app.include_router(api.router, prefix="/api", tags=["API"])

# 根路径
@app.get("/")
async def root():
    logger.info("🏠 访问根路径")
    return {
        "message": "欢迎使用 Demo FastAPI",
        "status": "运行中",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "timestamp": time.time()
    }

# 健康检查端点
@app.get("/health")
async def health_check():
    logger.debug("💓 执行健康检查")
    return {
        "status": "healthy",
        "message": "服务运行正常",
        "timestamp": time.time()
    }

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    method = request.method
    url = str(request.url)
    logger.error(f"🚨 全局异常捕获: {method} {url} | 错误类型: {type(exc).__name__} | 错误信息: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "内部服务器错误",
            "message": str(exc),
            "timestamp": time.time()
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )