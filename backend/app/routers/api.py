from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import datetime
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

# 导入子路由
from .auth import router as auth_router
from .users import router as users_router
from .roles import router as roles_router

# 注册子路由
logger.info("🔧 正在注册子路由...")
try:
    router.include_router(auth_router, prefix="/auth", tags=["认证"])
    logger.info("✅ 认证路由注册成功: /auth")

    router.include_router(users_router, prefix="/users", tags=["用户管理"])
    logger.info("✅ 用户管理路由注册成功: /users")

    router.include_router(roles_router, prefix="/roles", tags=["角色管理"])
    logger.info("✅ 角色管理路由注册成功: /roles")

    # 打印所有子路由信息用于调试
    logger.info("📋 所有子路由注册完成")

except Exception as e:
    logger.error(f"❌ 子路由注册失败: {str(e)}")
    raise

@router.get("/")
async def api_info():
    """获取 API 基本信息"""
    logger.info("📊 获取 API 基本信息")

    api_data = {
        "api_name": "Demo API",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "运行中"
    }

    logger.debug(f"📋 API 信息: {api_data}")
    return api_data


@router.post("/echo")
async def echo_message(data: Dict[str, Any]):
    """回显接收到的数据"""
    logger.info("📨 接收到回显请求")
    logger.debug(f"📦 接收数据: {data}")

    result = {
        "message": "数据接收成功",
        "received_data": data,
        "timestamp": datetime.datetime.now().isoformat()
    }

    logger.info("✅ 回显数据处理完成")
    logger.debug(f"📤 返回数据: {result}")

    return result