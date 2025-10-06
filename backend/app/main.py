from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime

from .core.config import settings
from .core.database import init_db
from .utils.logger import get_logger
from .utils.scheduler import scheduler, setup_default_tasks

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

        # 设置并启动定时任务
        setup_default_tasks()
        await scheduler.start()
        logger.info("定时任务调度器已启动")

        # 应用启动完成
        logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} 启动成功")
        logger.info(f"服务运行在: http://{settings.HOST}:{settings.PORT}")
        logger.info(f"API文档: http://{settings.HOST}:{settings.PORT}/docs")

    except Exception as e:
        logger.error(f"应用启动失败: {e}")
        raise

    yield

    # 关闭时执行
    logger.info("正在关闭定时任务调度器...")
    await scheduler.stop()
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
logger.info(f"🔧 CORS配置: 允许的源 - {settings.BACKEND_CORS_ORIGINS}")
logger.info(f"🔧 CORS配置: 当前DEBUG模式: {settings.DEBUG}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("✅ CORS中间件已配置")

# 用户上下文中间件（必须在审计日志中间件之前）
from .middleware import UserContextMiddleware, AuditLogMiddleware
app.add_middleware(UserContextMiddleware)
app.add_middleware(AuditLogMiddleware)

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

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """请求验证异常处理器"""
    logger.warning(f"请求验证错误: {exc.errors()} - {request.url}")
    return JSONResponse(
        status_code=422,
        content={
            "message": "请求数据验证失败",
            "detail": exc.errors(),
            "status_code": 422,
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

    # 添加路径调试信息
    path = request.url.path
    logger.info(f"🔍 请求路径解析: path='{path}', url='{url}'")

    # 检查可用路由
    available_routes = []
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            available_routes.append(f"{list(route.methods)} {route.path}")

    logger.info(f"📋 当前可用路由: {available_routes}")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        status_code = response.status_code

        # 记录性能数据
        from .utils.performance import performance_monitor
        performance_monitor.record_request(path, method, process_time, status_code)

        # 记录响应
        if status_code == 404:
            logger.warning(f"⚠️ 路由未找到: {method} {path}")
            logger.debug(f"🔍 尝试匹配的路由:")
            for route in app.routes:
                if hasattr(route, 'path') and hasattr(route, 'methods'):
                    if method in route.methods:
                        logger.debug(f"  - {method} {route.path}")

        logger.info(f"请求完成: {method} {url} - {status_code} - {process_time:.3f}s")

        # 添加响应头
        response.headers["X-Process-Time"] = str(process_time)

        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"请求失败: {method} {url} | 错误: {str(e)} | 耗时: {process_time:.3f}s")
        
        # 记录性能数据（失败的请求）
        from .utils.performance import performance_monitor
        performance_monitor.record_request(path, method, process_time, 500)
        
        raise

# 导入路由
from .routers import api

# 注册路由
logger.info("🔧 正在注册路由...")
try:
    app.include_router(api.router, prefix="/api", tags=["API"])
    logger.info("✅ 路由注册成功: /api")

    # 打印所有路由信息用于调试
    routes_info = []
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            routes_info.append(f"{list(route.methods)} {route.path}")

    logger.info(f"📋 已注册的路由列表: {routes_info}")

except Exception as e:
    logger.error(f"❌ 路由注册失败: {str(e)}")
    raise

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
        status = "ok"
    except Exception as e:
        status = "degraded"
        logger.error(f"数据库连接异常: {str(e)}")

    return {
        "status": status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": settings.APP_VERSION
    }

# 调度器状态
@app.get("/api/scheduler/status", response_model=dict)
async def scheduler_status():
    """获取调度器状态"""
    try:
        status = scheduler.get_status()
        return {
            "success": True,
            "data": status
        }
    except Exception as e:
        logger.error(f"获取调度器状态失败: {str(e)}")
        return {
            "success": False,
            "message": f"获取调度器状态失败: {str(e)}"
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