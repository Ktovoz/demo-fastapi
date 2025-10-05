from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timedelta
from typing import Dict, Any, List
import random

from ..core.database import get_db
from ..models.user import User
from ..models.operation_log import OperationLog
from ..utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/metrics")
async def get_dashboard_metrics(db: Session = Depends(get_db)):
    """获取仪表盘核心数据"""
    logger.info("获取仪表盘数据")
    
    try:
        # 获取用户总数
        total_users = db.query(User).count()
        
        # 获取活跃用户数（最近7天有登录）
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        active_users = db.query(User).filter(User.last_login >= seven_days_ago).count()
        
        # 获取系统总请求数（从操作日志中统计）
        total_requests = db.query(OperationLog).count()
        
        # 获取今日请求数
        today = datetime.utcnow().date()
        today_requests = db.query(OperationLog).filter(
            OperationLog.created_at >= today
        ).count()
        
        # 获取错误请求数
        error_requests = db.query(OperationLog).filter(
            OperationLog.action.like('%ERROR%')
        ).count()
        
        # 生成流量图表数据（最近7天）
        traffic_chart = {"labels": [], "series": []}
        api_requests_data = []
        active_users_data = []
        
        for i in range(7):
            date = (datetime.utcnow() - timedelta(days=6-i)).date()
            date_str = date.strftime("%m-%d")
            traffic_chart["labels"].append(date_str)
            
            # 模拟API请求数据
            requests_count = random.randint(1500, 2000)
            api_requests_data.append(requests_count)
            
            # 模拟活跃用户数据
            users_count = random.randint(500, 800)
            active_users_data.append(users_count)
        
        traffic_chart["series"] = [
            {"name": "API Requests", "data": api_requests_data},
            {"name": "Active Users", "data": active_users_data}
        ]
        
        # 生成系统健康状态
        system_health = [
            {
                "label": "API服务",
                "status": "operational",
                "message": "所有系统运行正常"
            },
            {
                "label": "数据库",
                "status": "operational",
                "message": "数据库连接正常"
            },
            {
                "label": "缓存服务",
                "status": "degraded",
                "message": "响应时间略高于预期"
            },
            {
                "label": "认证服务",
                "status": "operational",
                "message": "认证系统运行正常"
            }
        ]
        
        # 生成最近活动
        recent_activities = []
        recent_logs = db.query(OperationLog).order_by(
            OperationLog.created_at.desc()
        ).limit(5).all()
        
        for log in recent_logs:
            recent_activities.append({
                "id": f"LOG-{log.id}",
                "time": log.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "user": log.user.full_name if log.user else "系统",
                "action": log.action,
                "target": log.resource
            })
        
        # 如果没有足够的日志，添加一些模拟数据
        if len(recent_activities) < 5:
            mock_activities = [
                {
                    "id": "LOG-MOCK-1",
                    "time": (datetime.utcnow() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
                    "user": "张三",
                    "action": "登录系统",
                    "target": "/auth/login"
                },
                {
                    "id": "LOG-MOCK-2",
                    "time": (datetime.utcnow() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
                    "user": "李四",
                    "action": "查看用户列表",
                    "target": "/users"
                },
                {
                    "id": "LOG-MOCK-3",
                    "time": (datetime.utcnow() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
                    "user": "王五",
                    "action": "更新角色权限",
                    "target": "/roles/1"
                },
                {
                    "id": "LOG-MOCK-4",
                    "time": (datetime.utcnow() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
                    "user": "赵六",
                    "action": "导出数据报表",
                    "target": "/reports/export"
                },
                {
                    "id": "LOG-MOCK-5",
                    "time": (datetime.utcnow() - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S"),
                    "user": "系统",
                    "action": "定时备份",
                    "target": "/system/backup"
                }
            ]
            
            # 添加模拟数据直到有5条记录
            while len(recent_activities) < 5:
                recent_activities.append(mock_activities[5 - len(recent_activities) - 1])
        
        # 生成摘要卡片数据
        summary_cards = [
            {
                "key": "users",
                "title": "总用户数",
                "value": total_users,
                "unit": "人",
                "change": random.randint(5, 15),
                "changeType": "increase",
                "trend": "up",
                "trendLabel": "较上周",
                "description": "注册用户总数",
                "icon": "TeamOutlined"
            },
            {
                "key": "activeUsers",
                "title": "活跃用户",
                "value": active_users,
                "unit": "人",
                "change": random.randint(-5, 10),
                "changeType": "increase" if random.random() > 0.3 else "decrease",
                "trend": "up" if random.random() > 0.3 else "down",
                "trendLabel": "较上周",
                "description": "7天内活跃用户",
                "icon": "RiseOutlined"
            },
            {
                "key": "requests",
                "title": "API请求",
                "value": total_requests,
                "unit": "次",
                "change": random.randint(10, 25),
                "changeType": "increase",
                "trend": "up",
                "trendLabel": "较昨日",
                "description": "累计API请求次数",
                "icon": "DashboardOutlined"
            },
            {
                "key": "errors",
                "title": "错误请求",
                "value": error_requests,
                "unit": "次",
                "change": random.randint(-10, 5),
                "changeType": "decrease" if random.random() > 0.4 else "increase",
                "trend": "down" if random.random() > 0.4 else "up",
                "trendLabel": "较昨日",
                "description": "系统错误次数",
                "icon": "AlertOutlined"
            }
        ]
        
        result = {
            "summaryCards": summary_cards,
            "trafficChart": traffic_chart,
            "systemHealth": system_health,
            "recentActivities": recent_activities
        }
        
        logger.info("仪表盘数据获取成功")
        return result
        
    except Exception as e:
        logger.error(f"获取仪表盘数据失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取仪表盘数据失败"
        )

@router.get("/overview")
async def get_dashboard_overview(db: Session = Depends(get_db)):
    """获取仪表盘概览数据"""
    logger.info("获取仪表盘概览数据")
    
    try:
        # 这个接口与metrics接口返回相同的数据，用于渐进式加载
        return await get_dashboard_metrics(db)
    except Exception as e:
        logger.error(f"获取仪表盘概览数据失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取仪表盘概览数据失败"
        )