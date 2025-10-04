from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入路由
from app.routers import api

# 创建 FastAPI 应用实例
app = FastAPI(
    title=os.getenv("APP_NAME", "Demo FastAPI"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="一个前后端分离的示例项目",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # 允许的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(api.router, prefix="/api", tags=["API"])

# 根路径
@app.get("/")
async def root():
    return {
        "message": "欢迎使用 Demo FastAPI",
        "status": "运行中",
        "version": os.getenv("APP_VERSION", "1.0.0")
    }

# 健康检查端点
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "服务运行正常"
    }

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "内部服务器错误",
            "message": str(exc)
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )