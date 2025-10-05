from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import datetime
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

# 导入子路由
from .auth import router as auth_router
from .dashboard import router as dashboard_router
from .users import router as users_router
from .roles import router as roles_router
from .admin import router as admin_router
from .system import router as system_router

# 注册子路由
logger.info("🔧 正在注册子路由...")
try:
    router.include_router(auth_router, prefix="/auth", tags=["认证"])
    logger.info("✅ 认证路由注册成功: /auth")

    router.include_router(dashboard_router, prefix="/dashboard", tags=["仪表盘"])
    logger.info("✅ 仪表盘路由注册成功: /dashboard")

    router.include_router(users_router, prefix="/users", tags=["用户管理"])
    logger.info("✅ 用户管理路由注册成功: /users")

    router.include_router(roles_router, prefix="/roles", tags=["角色管理"])
    logger.info("✅ 角色管理路由注册成功: /roles")

    router.include_router(admin_router, prefix="/admin", tags=["运营中心"])
    logger.info("✅ 运营中心路由注册成功: /admin")

    router.include_router(system_router, prefix="/system", tags=["系统管理"])
    logger.info("✅ 系统管理路由注册成功: /system")

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

@router.get("/users")
async def get_users():
    """获取用户列表示例"""
    logger.info("👥 获取用户列表")

    users = [
        {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
        {"id": 2, "name": "李四", "email": "lisi@example.com"},
        {"id": 3, "name": "王五", "email": "wangwu@example.com"}
    ]

    result = {
        "users": users,
        "total": len(users)
    }

    logger.info(f"👥 返回用户列表: 共 {len(users)} 个用户")
    logger.debug(f"📋 用户详情: {users}")

    return result

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    """根据 ID 获取用户信息"""
    logger.info(f"🔍 查询用户信息: user_id={user_id}")

    users = {
        1: {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
        2: {"id": 2, "name": "李四", "email": "lisi@example.com"},
        3: {"id": 3, "name": "王五", "email": "wangwu@example.com"}
    }

    if user_id < 1 or user_id > 3:
        logger.warning(f"⚠️ 用户不存在: user_id={user_id}")
        raise HTTPException(status_code=404, detail="用户不存在")

    user_data = users[user_id]
    logger.info(f"✅ 找到用户: {user_data['name']} (ID: {user_id})")
    logger.debug(f"📋 用户详情: {user_data}")

    return user_data

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