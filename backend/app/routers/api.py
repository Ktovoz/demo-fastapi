from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import datetime

router = APIRouter()

@router.get("/")
async def api_info():
    """获取 API 基本信息"""
    return {
        "api_name": "Demo API",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "运行中"
    }

@router.get("/users")
async def get_users():
    """获取用户列表示例"""
    return {
        "users": [
            {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
            {"id": 2, "name": "李四", "email": "lisi@example.com"},
            {"id": 3, "name": "王五", "email": "wangwu@example.com"}
        ],
        "total": 3
    }

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    """根据 ID 获取用户信息"""
    if user_id < 1 or user_id > 3:
        raise HTTPException(status_code=404, detail="用户不存在")

    users = {
        1: {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
        2: {"id": 2, "name": "李四", "email": "lisi@example.com"},
        3: {"id": 3, "name": "王五", "email": "wangwu@example.com"}
    }

    return users[user_id]

@router.post("/echo")
async def echo_message(data: Dict[str, Any]):
    """回显接收到的数据"""
    return {
        "message": "数据接收成功",
        "received_data": data,
        "timestamp": datetime.datetime.now().isoformat()
    }