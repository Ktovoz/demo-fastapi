from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime

from .core.config import settings
from .core.database import init_db
from .utils.logger import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("后台管理系统启动中...")

    try:
        # 初始化数据库
        init_db()
        logger.info("数据库初始化完成")

        # 应用启动完成
        logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} 启动成功")
        logger.info(f"服务运行在: http://{settings.HOST}:{settings.PORT}")
        logger.info(f"API文档: http://{settings.HOST}:{settings.PORT}/docs")

    except Exception as e:
        logger.error(f"应用启动失败: {e}")
        raise

    yield

    # 关闭时执行
    logger.info("后台管理系统正在关闭...")

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="基于FastAPI + Vue3的后台管理系统Demo",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP异常处理器"""
    logger.warning(f"HTTP异常: {exc.status_code} - {exc.detail} - {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    logger.error(f"未处理的异常: {type(exc).__name__} - {str(exc)} - {request.url}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "服务器内部错误" if not settings.DEBUG else str(exc),
            "status_code": 500,
            "path": str(request.url)
        }
    )

# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """请求日志中间件"""
    import time
    start_time = time.time()

    # 记录请求
    client_ip = request.client.host
    method = request.method
    url = str(request.url)
    user_agent = request.headers.get("user-agent", "Unknown")

    logger.info(f"请求开始: {method} {url} | 客户端: {client_ip} | User-Agent: {user_agent}")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        status_code = response.status_code

        # 记录响应
        logger.info(f"请求完成: {method} {url} - {status_code} - {process_time:.3f}s")

        # 添加响应头
        response.headers["X-Process-Time"] = str(process_time)

        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"请求失败: {method} {url} | 错误: {str(e)} | 耗时: {process_time:.3f}s")
        raise

# 导入路由
try:
    from .routers import api
except ImportError:
    from routers import api

# 注册路由
app.include_router(api.router, prefix="/api", tags=["API"])

# 根路径
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": f"欢迎使用{settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

# 健康检查
@app.get("/health", response_model=dict)
async def health_check():
    """健康检查"""
    logger.debug("执行健康检查")
    
    # 检查数据库连接状态
    try:
        from .core.database import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        database_status = "healthy"
    except Exception as e:
        database_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy",
        "message": "服务运行正常",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "database_status": database_status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )