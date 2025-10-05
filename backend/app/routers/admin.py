from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random
import json

from ..core.database import get_db
from ..models.user import User
from ..models.operation_log import OperationLog
from ..utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/overview")
async def get_admin_overview(db: Session = Depends(get_db)):
    """获取运营总览数据"""
    logger.info("获取运营总览数据")
    
    try:
        # 获取用户总数
        total_users = db.query(User).count()
        
        # 获取今日新增用户
        today = datetime.utcnow().date()
        today_new_users = db.query(User).filter(User.created_at >= today).count()
        
        # 获取活跃用户数（最近7天有登录）
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        active_users = db.query(User).filter(User.last_login >= seven_days_ago).count()
        
        # 获取系统总请求数（从操作日志中统计）
        total_requests = db.query(OperationLog).count()
        
        # 获取今日请求数
        today_requests = db.query(OperationLog).filter(
            OperationLog.created_at >= today
        ).count()
        
        # 生成仪表卡片数据
        cards = [
            {
                "key": "users",
                "title": "总用户数",
                "value": total_users,
                "unit": "人",
                "change": random.randint(5, 15),
                "changeType": "increase",
                "description": "注册用户总数",
                "icon": "TeamOutlined",
                "trendLabel": "较上周"
            },
            {
                "key": "newUsers",
                "title": "今日新增",
                "value": today_new_users,
                "unit": "人",
                "change": random.randint(-10, 20),
                "changeType": "increase" if random.random() > 0.3 else "decrease",
                "description": "今日注册用户",
                "icon": "UserAddOutlined",
                "trendLabel": "较昨日"
            },
            {
                "key": "activeUsers",
                "title": "活跃用户",
                "value": active_users,
                "unit": "人",
                "change": random.randint(-5, 10),
                "changeType": "increase" if random.random() > 0.3 else "decrease",
                "description": "7天内活跃用户",
                "icon": "RiseOutlined",
                "trendLabel": "较上周"
            },
            {
                "key": "requests",
                "title": "API请求",
                "value": total_requests,
                "unit": "次",
                "change": random.randint(10, 25),
                "changeType": "increase",
                "description": "累计API请求次数",
                "icon": "DashboardOutlined",
                "trendLabel": "较昨日"
            }
        ]
        
        # 生成趋势数据（最近7天）
        trend = []
        for i in range(7):
            date = datetime.utcnow() - timedelta(days=6-i)
            date_str = date.strftime("%m-%d")
            
            # 模拟数据
            requests_count = random.randint(15000, 20000)
            active_users_count = random.randint(800, 1200)
            error_rate = round(random.uniform(0.1, 0.8), 2)
            
            trend.append({
                "date": date_str,
                "requests": requests_count,
                "activeUsers": active_users_count,
                "errorRate": error_rate
            })
        
        # 生成服务状态数据
        services = [
            {
                "key": "api",
                "name": "API服务",
                "owner": "技术团队",
                "status": "operational",
                "uptime": 99.9,
                "latency": 120,
                "change": random.uniform(-5, 5)
            },
            {
                "key": "database",
                "name": "数据库服务",
                "owner": "运维团队",
                "status": "operational",
                "uptime": 99.8,
                "latency": 45,
                "change": random.uniform(-5, 5)
            },
            {
                "key": "cache",
                "name": "缓存服务",
                "owner": "技术团队",
                "status": "degraded",
                "uptime": 98.5,
                "latency": 25,
                "change": random.uniform(-5, 5)
            },
            {
                "key": "storage",
                "name": "存储服务",
                "owner": "运维团队",
                "status": "operational",
                "uptime": 99.7,
                "latency": 85,
                "change": random.uniform(-5, 5)
            }
        ]
        
        # 生成值班信息
        shifts = [
            {
                "id": "shift-1",
                "name": "早班",
                "window": "08:00-16:00",
                "lead": "张三",
                "readiness": round(random.uniform(0.8, 1.0), 2)
            },
            {
                "id": "shift-2",
                "name": "中班",
                "window": "16:00-00:00",
                "lead": "李四",
                "readiness": round(random.uniform(0.8, 1.0), 2)
            },
            {
                "id": "shift-3",
                "name": "夜班",
                "window": "00:00-08:00",
                "lead": "王五",
                "readiness": round(random.uniform(0.7, 0.9), 2)
            }
        ]
        
        result = {
            "cards": cards,
            "trend": trend,
            "services": services,
            "shifts": shifts
        }
        
        logger.info("获取运营总览数据成功")
        return result
        
    except Exception as e:
        logger.error(f"获取运营总览数据失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取运营总览数据失败"
        )

@router.get("/alerts")
async def get_alerts(db: Session = Depends(get_db)):
    """获取告警列表"""
    logger.info("获取告警列表")
    
    try:
        # 模拟告警数据
        alerts = [
            {
                "id": "alert-1",
                "severity": "high",
                "title": "API服务响应时间异常",
                "message": "API服务平均响应时间超过500ms阈值",
                "timestamp": (datetime.utcnow() - timedelta(minutes=30)).isoformat() + "Z",
                "owner": "技术团队",
                "acknowledged": False
            },
            {
                "id": "alert-2",
                "severity": "medium",
                "title": "数据库连接数接近上限",
                "message": "数据库连接数已达到80%，请及时处理",
                "timestamp": (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z",
                "owner": "运维团队",
                "acknowledged": True
            },
            {
                "id": "alert-3",
                "severity": "low",
                "title": "缓存服务内存使用率高",
                "message": "缓存服务内存使用率达到75%",
                "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat() + "Z",
                "owner": "技术团队",
                "acknowledged": False
            },
            {
                "id": "alert-4",
                "severity": "medium",
                "title": "用户登录失败率上升",
                "message": "最近1小时用户登录失败率达到5%",
                "timestamp": (datetime.utcnow() - timedelta(hours=3)).isoformat() + "Z",
                "owner": "安全团队",
                "acknowledged": True
            },
            {
                "id": "alert-5",
                "severity": "low",
                "title": "日志存储空间不足",
                "message": "日志存储空间剩余20%，预计2天后耗尽",
                "timestamp": (datetime.utcnow() - timedelta(hours=4)).isoformat() + "Z",
                "owner": "运维团队",
                "acknowledged": False
            }
        ]
        
        logger.info(f"获取告警列表成功: 共 {len(alerts)} 条告警")
        return alerts
        
    except Exception as e:
        logger.error(f"获取告警列表失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取告警列表失败"
        )

@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    db: Session = Depends(get_db)
):
    """确认告警"""
    logger.info(f"确认告警: {alert_id}")
    
    try:
        # 在实际应用中，这里应该更新数据库中的告警状态
        # 由于我们没有告警表，这里只是模拟操作
        
        # 模拟告警数据
        alerts = {
            "alert-1": {
                "id": "alert-1",
                "severity": "high",
                "title": "API服务响应时间异常",
                "message": "API服务平均响应时间超过500ms阈值",
                "timestamp": (datetime.utcnow() - timedelta(minutes=30)).isoformat() + "Z",
                "owner": "技术团队",
                "acknowledged": True
            },
            "alert-2": {
                "id": "alert-2",
                "severity": "medium",
                "title": "数据库连接数接近上限",
                "message": "数据库连接数已达到80%，请及时处理",
                "timestamp": (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z",
                "owner": "运维团队",
                "acknowledged": True
            }
        }
        
        if alert_id not in alerts:
            raise HTTPException(
                status_code=404,
                detail="告警不存在"
            )
        
        logger.info(f"告警确认成功: {alert_id}")
        return alerts[alert_id]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"确认告警失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="确认告警失败"
        )

@router.get("/tasks")
async def get_tasks(
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(6, ge=1, le=20, description="每页数量"),
    status: Optional[str] = Query("all", description="状态筛选"),
    priority: Optional[str] = Query("all", description="优先级筛选"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    tags: Optional[str] = Query(None, description="标签筛选"),
    sorter: Optional[str] = Query(None, description="排序"),
    db: Session = Depends(get_db)
):
    """获取任务列表"""
    logger.info(f"获取任务列表: page={page}, pageSize={pageSize}")
    
    try:
        # 模拟任务数据
        all_tasks = [
            {
                "id": "task-1",
                "title": "优化API响应时间",
                "assignee": "张三",
                "due": (datetime.utcnow() + timedelta(days=2)).date().isoformat(),
                "priority": "high",
                "status": "in_progress",
                "tags": ["性能优化", "后端"],
                "avatarColor": "#f50"
            },
            {
                "id": "task-2",
                "title": "修复用户登录异常",
                "assignee": "李四",
                "due": (datetime.utcnow() + timedelta(days=1)).date().isoformat(),
                "priority": "high",
                "status": "todo",
                "tags": ["Bug修复", "安全"],
                "avatarColor": "#2db7f5"
            },
            {
                "id": "task-3",
                "title": "更新用户文档",
                "assignee": "王五",
                "due": (datetime.utcnow() + timedelta(days=5)).date().isoformat(),
                "priority": "medium",
                "status": "review",
                "tags": ["文档", "用户体验"],
                "avatarColor": "#87d068"
            },
            {
                "id": "task-4",
                "title": "添加数据备份功能",
                "assignee": "赵六",
                "due": (datetime.utcnow() + timedelta(days=7)).date().isoformat(),
                "priority": "medium",
                "status": "todo",
                "tags": ["运维", "数据安全"],
                "avatarColor": "#108ee9"
            },
            {
                "id": "task-5",
                "title": "优化数据库查询",
                "assignee": "钱七",
                "due": (datetime.utcnow() + timedelta(days=3)).date().isoformat(),
                "priority": "low",
                "status": "done",
                "tags": ["性能优化", "数据库"],
                "avatarColor": "#f56a00"
            },
            {
                "id": "task-6",
                "title": "实现用户权限管理",
                "assignee": "孙八",
                "due": (datetime.utcnow() + timedelta(days=10)).date().isoformat(),
                "priority": "high",
                "status": "in_progress",
                "tags": ["功能开发", "权限"],
                "avatarColor": "#722ed1"
            },
            {
                "id": "task-7",
                "title": "设计新版本UI",
                "assignee": "周九",
                "due": (datetime.utcnow() + timedelta(days=14)).date().isoformat(),
                "priority": "medium",
                "status": "todo",
                "tags": ["设计", "UI/UX"],
                "avatarColor": "#eb2f96"
            },
            {
                "id": "task-8",
                "title": "系统安全审计",
                "assignee": "吴十",
                "due": (datetime.utcnow() + timedelta(days=21)).date().isoformat(),
                "priority": "high",
                "status": "todo",
                "tags": ["安全", "审计"],
                "avatarColor": "#13c2c2"
            }
        ]
        
        # 应用筛选条件
        filtered_tasks = all_tasks
        
        if status != "all":
            filtered_tasks = [task for task in filtered_tasks if task["status"] == status]
        
        if priority != "all":
            filtered_tasks = [task for task in filtered_tasks if task["priority"] == priority]
        
        if keyword:
            filtered_tasks = [
                task for task in filtered_tasks 
                if keyword.lower() in task["title"].lower() or keyword.lower() in task["assignee"].lower()
            ]
        
        if tags:
            tag_list = tags.split(",") if isinstance(tags, str) else tags
            filtered_tasks = [
                task for task in filtered_tasks 
                if any(tag in task["tags"] for tag in tag_list)
            ]
        
        # 计算总数
        total = len(filtered_tasks)
        
        # 分页
        start = (page - 1) * pageSize
        end = start + pageSize
        tasks = filtered_tasks[start:end]
        
        result = {
            "items": tasks,
            "total": total,
            "page": page,
            "pageSize": pageSize
        }
        
        logger.info(f"获取任务列表成功: 共 {total} 条记录")
        return result
        
    except Exception as e:
        logger.error(f"获取任务列表失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取任务列表失败"
        )

@router.post("/tasks")
async def create_task(
    task_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """创建任务"""
    logger.info(f"创建任务: {task_data.get('title')}")
    
    try:
        # 验证必填字段
        if "title" not in task_data or not task_data["title"]:
            raise HTTPException(
                status_code=400,
                detail="任务标题不能为空"
            )
        
        if "assignee" not in task_data or not task_data["assignee"]:
            raise HTTPException(
                status_code=400,
                detail="任务负责人不能为空"
            )
        
        if "priority" not in task_data or not task_data["priority"]:
            raise HTTPException(
                status_code=400,
                detail="任务优先级不能为空"
            )
        
        if "status" not in task_data or not task_data["status"]:
            task_data["status"] = "todo"  # 默认状态
        
        # 生成任务ID
        import random
        task_id = f"task-{random.randint(1000, 9999)}"
        
        # 设置默认值
        if "tags" not in task_data:
            task_data["tags"] = []
        
        if "avatarColor" not in task_data:
            colors = ["#f50", "#2db7f5", "#87d068", "#108ee9", "#f56a00", "#722ed1", "#eb2f96", "#13c2c2"]
            task_data["avatarColor"] = random.choice(colors)
        
        if "due" not in task_data:
            task_data["due"] = (datetime.utcnow() + timedelta(days=7)).date().isoformat()
        
        # 构建任务数据
        new_task = {
            "id": task_id,
            "title": task_data["title"],
            "assignee": task_data["assignee"],
            "due": task_data["due"],
            "priority": task_data["priority"],
            "status": task_data["status"],
            "tags": task_data["tags"],
            "avatarColor": task_data["avatarColor"]
        }
        
        logger.info(f"任务创建成功: {task_id}")
        return new_task
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建任务失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="创建任务失败"
        )

@router.patch("/tasks/{task_id}")
async def update_task(
    task_id: str,
    task_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """更新任务"""
    logger.info(f"更新任务: {task_id}")
    
    try:
        # 在实际应用中，这里应该更新数据库中的任务信息
        # 由于我们没有任务表，这里只是模拟操作
        
        # 模拟任务数据
        tasks = {
            "task-1": {
                "id": "task-1",
                "title": "优化API响应时间",
                "assignee": "张三",
                "due": (datetime.utcnow() + timedelta(days=2)).date().isoformat(),
                "priority": "high",
                "status": "in_progress",
                "tags": ["性能优化", "后端"],
                "avatarColor": "#f50"
            },
            "task-2": {
                "id": "task-2",
                "title": "修复用户登录异常",
                "assignee": "李四",
                "due": (datetime.utcnow() + timedelta(days=1)).date().isoformat(),
                "priority": "high",
                "status": "todo",
                "tags": ["Bug修复", "安全"],
                "avatarColor": "#2db7f5"
            }
        }
        
        if task_id not in tasks:
            raise HTTPException(
                status_code=404,
                detail="任务不存在"
            )
        
        # 更新任务信息
        task = tasks[task_id]
        for key, value in task_data.items():
            if key in task:
                task[key] = value
        
        logger.info(f"任务更新成功: {task_id}")
        return task
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新任务失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="更新任务失败"
        )

@router.get("/audit-timeline")
async def get_audit_timeline(db: Session = Depends(get_db)):
    """获取审计时间线"""
    logger.info("获取审计时间线")

    try:
        # 首先尝试获取操作日志
        timeline = []
        try:
            logger.debug("开始查询操作日志")
            logs = db.query(OperationLog).order_by(OperationLog.created_at.desc()).limit(20).all()
            logger.debug(f"查询到 {len(logs)} 条操作日志")

            # 构建审计时间线数据
            for i, log in enumerate(logs):
                try:
                    logger.debug(f"处理第 {i+1} 条日志，ID: {log.id}")

                    # 安全地获取用户信息
                    actor = "匿名用户"
                    if log.user_id:
                        if log.user:
                            actor = log.user.full_name or f"用户{log.user_id}"
                        else:
                            actor = f"用户{log.user_id}"
                            # 尝试从数据库重新获取用户信息
                            try:
                                user = db.query(User).filter(User.id == log.user_id).first()
                                if user:
                                    actor = user.full_name or f"用户{log.user_id}"
                            except Exception as user_error:
                                logger.warning(f"获取用户 {log.user_id} 信息失败: {str(user_error)}")

                    # 确定操作状态（基于描述判断）
                    status = "success"
                    description = log.description or ""
                    if "失败" in description or "错误" in description:
                        status = "failed"
                    elif "警告" in description or "超时" in description:
                        status = "warning"

                    # 构建审计项
                    audit_item = {
                        "id": f"audit-{log.id}",
                        "time": log.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "actor": actor,
                        "action": log.action or "未知操作",
                        "target": log.resource or "未知资源",
                        "detail": description or f"{log.action or '未知操作'} {log.resource or '未知资源'}",
                        "status": status,
                        "ip_address": log.ip_address or "未知"
                    }

                    timeline.append(audit_item)
                    logger.debug(f"成功处理日志 {log.id}")

                except Exception as log_error:
                    logger.error(f"处理日志 {getattr(log, 'id', 'unknown')} 时出错: {str(log_error)}")
                    continue

        except Exception as db_error:
            logger.warning(f"数据库查询失败，使用模拟数据: {str(db_error)}")
        
        # 如果没有足够的日志，添加一些模拟数据
        if len(timeline) < 10:
            mock_audits = [
                {
                    "id": "audit-mock-1",
                    "time": (datetime.utcnow() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
                    "actor": "张三",
                    "action": "登录系统",
                    "target": "/auth/login",
                    "detail": "用户登录成功",
                    "status": "success"
                },
                {
                    "id": "audit-mock-2",
                    "time": (datetime.utcnow() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
                    "actor": "李四",
                    "action": "查看用户列表",
                    "target": "/users",
                    "detail": "获取用户列表",
                    "status": "success"
                },
                {
                    "id": "audit-mock-3",
                    "time": (datetime.utcnow() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
                    "actor": "王五",
                    "action": "更新角色权限",
                    "target": "/roles/1",
                    "detail": "修改角色权限配置",
                    "status": "success"
                },
                {
                    "id": "audit-mock-4",
                    "time": (datetime.utcnow() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
                    "actor": "赵六",
                    "action": "删除用户",
                    "target": "/users/123",
                    "detail": "删除用户账号",
                    "status": "warning"
                },
                {
                    "id": "audit-mock-5",
                    "time": (datetime.utcnow() - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S"),
                    "actor": "系统",
                    "action": "数据备份",
                    "target": "/system/backup",
                    "detail": "执行定时数据备份",
                    "status": "success"
                }
            ]
            
            # 添加模拟数据直到有10条记录
            while len(timeline) < 10:
                timeline.append(mock_audits[5 - len(timeline) - 1])
        
        logger.info(f"获取审计时间线成功: 共 {len(timeline)} 条记录")
        return timeline

    except Exception as e:
        import traceback
        logger.error(f"获取审计时间线失败: {str(e)}")
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"获取审计时间线失败: {str(e)}"
        )