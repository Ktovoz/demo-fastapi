from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text, or_, and_, func
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
import random

from ..core.database import get_db
from ..models.operation_log import OperationLog
from ..utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/logs")
async def get_system_logs(
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    level: Optional[str] = Query("ALL", description="日志级别筛选"),
    sorter: Optional[str] = Query(None, description="排序"),
    db: Session = Depends(get_db)
):
    """获取系统日志"""
    logger.info(f"获取系统日志: page={page}, pageSize={pageSize}, keyword={keyword}, level={level}")
    
    try:
        # 构建查询
        query = db.query(OperationLog)
        
        # 关键词搜索
        if keyword:
            query = query.filter(
                or_(
                    OperationLog.method.like(f"%{keyword}%"),
                    OperationLog.path.like(f"%{keyword}%"),
                    OperationLog.ip.like(f"%{keyword}%")
                )
            )
        
        # 级别筛选
        if level != "ALL":
            # 这里假设OperationLog模型有level字段，如果没有，可以基于其他逻辑
            # 例如根据method或status_code判断级别
            if level == "ERROR":
                query = query.filter(or_(
                    OperationLog.method.like("%ERROR%"),
                    OperationLog.status_code >= 400
                ))
            elif level == "WARN":
                query = query.filter(and_(
                    OperationLog.method.notlike("%ERROR%"),
                    or_(
                        OperationLog.method.like("%WARN%"),
                        and_(OperationLog.status_code >= 300, OperationLog.status_code < 400)
                    )
                ))
            elif level == "INFO":
                query = query.filter(and_(
                    OperationLog.method.notlike("%ERROR%"),
                    OperationLog.method.notlike("%WARN%"),
                    OperationLog.status_code < 300
                ))
        
        # 排序处理
        if sorter:
            try:
                sorter_data = json.loads(sorter) if isinstance(sorter, str) else sorter
                field = sorter_data.get("field", "time")
                order = sorter_data.get("order", "descend")
                
                # 映射字段名
                field_mapping = {
                    "time": OperationLog.created_at,
                    "method": OperationLog.method,
                    "path": OperationLog.path
                }
                
                if field in field_mapping:
                    if order == "descend":
                        query = query.order_by(field_mapping[field].desc())
                    else:
                        query = query.order_by(field_mapping[field].asc())
            except Exception as e:
                logger.warning(f"排序参数解析失败: {str(e)}")
                # 使用默认排序
                query = query.order_by(OperationLog.created_at.desc())
        else:
            # 默认按时间倒序
            query = query.order_by(OperationLog.created_at.desc())
        
        # 计算总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * pageSize
        logs = query.offset(offset).limit(pageSize).all()
        
        # 构建返回数据
        items = []
        for log in logs:
            # 确定日志级别
            log_level = "INFO"
            if "ERROR" in log.method.upper() or log.status_code >= 400:
                log_level = "ERROR"
            elif "WARN" in log.method.upper() or (log.status_code >= 300 and log.status_code < 400):
                log_level = "WARN"
            elif "DEBUG" in log.method.upper():
                log_level = "DEBUG"
            
            # 构建上下文信息
            context = {
                "requestId": f"req-{log.id}",
                "ip": log.ip,
                "userAgent": log.user_agent,
                "statusCode": log.status_code
            }
            
            # 构建日志数据
            log_data = {
                "id": f"LOG-{log.id}",
                "time": log.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "level": log_level,
                "module": log.method.split()[0] if log.method and " " in log.method else "system",
                "message": f"{log.method} {log.path}",
                "context": context
            }
            
            items.append(log_data)
        
        # 如果没有足够的日志，添加一些模拟数据
        if len(items) < 5:
            mock_logs = [
                {
                    "id": "LOG-MOCK-1",
                    "time": (datetime.utcnow() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
                    "level": "ERROR",
                    "module": "billing",
                    "message": "Payment webhook failed",
                    "context": {
                        "requestId": "req-1a2b3c",
                        "ip": "203.0.113.10"
                    }
                },
                {
                    "id": "LOG-MOCK-2",
                    "time": (datetime.utcnow() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
                    "level": "WARN",
                    "module": "auth",
                    "message": "Multiple failed login attempts",
                    "context": {
                        "requestId": "req-4d5e6f",
                        "ip": "192.0.2.45"
                    }
                },
                {
                    "id": "LOG-MOCK-3",
                    "time": (datetime.utcnow() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
                    "level": "INFO",
                    "module": "user",
                    "message": "User profile updated",
                    "context": {
                        "requestId": "req-7g8h9i",
                        "ip": "198.51.100.22"
                    }
                },
                {
                    "id": "LOG-MOCK-4",
                    "time": (datetime.utcnow() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
                    "level": "ERROR",
                    "module": "notifications",
                    "message": "Provider timeout",
                    "context": {
                        "requestId": "req-0j1k2l",
                        "ip": "203.0.113.55"
                    }
                },
                {
                    "id": "LOG-MOCK-5",
                    "time": (datetime.utcnow() - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S"),
                    "level": "DEBUG",
                    "module": "system",
                    "message": "Cache cleanup completed",
                    "context": {
                        "requestId": "req-3m4n5o",
                        "ip": "192.0.2.99"
                    }
                }
            ]
            
            # 添加模拟数据直到有5条记录
            while len(items) < 5:
                items.append(mock_logs[5 - len(items) - 1])
        
        result = {
            "items": items,
            "total": total,
            "page": page,
            "pageSize": pageSize
        }
        
        logger.info(f"获取系统日志成功: 共 {total} 条记录")
        return result
        
    except Exception as e:
        logger.error(f"获取系统日志失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取系统日志失败"
        )

@router.get("/logs/summary")
async def get_logs_summary(db: Session = Depends(get_db)):
    """获取日志概览数据"""
    logger.info("获取日志概览数据")
    
    try:
        # 获取总日志数
        total_logs = db.query(OperationLog).count()
        
        # 获取各级别日志数量
        error_count = db.query(OperationLog).filter(or_(
            OperationLog.method.like("%ERROR%"),
            OperationLog.status_code >= 400
        )).count()
        
        warn_count = db.query(OperationLog).filter(and_(
            OperationLog.method.notlike("%ERROR%"),
            or_(
                OperationLog.method.like("%WARN%"),
                and_(OperationLog.status_code >= 300, OperationLog.status_code < 400)
            )
        )).count()
        
        info_count = db.query(OperationLog).filter(and_(
            OperationLog.method.notlike("%ERROR%"),
            OperationLog.method.notlike("%WARN%"),
            OperationLog.status_code < 300
        )).count()
        
        debug_count = db.query(OperationLog).filter(OperationLog.method.like("%DEBUG%")).count()
        
        # 构建严重程度统计
        severity = {
            "ERROR": error_count,
            "WARN": warn_count,
            "INFO": info_count,
            "DEBUG": debug_count
        }
        
        # 获取最近日志
        recent_logs = db.query(OperationLog).order_by(OperationLog.created_at.desc()).limit(5).all()
        recent = []
        
        for log in recent_logs:
            # 确定日志级别
            log_level = "INFO"
            if "ERROR" in log.method.upper() or log.status_code >= 400:
                log_level = "ERROR"
            elif "WARN" in log.method.upper() or (log.status_code >= 300 and log.status_code < 400):
                log_level = "WARN"
            elif "DEBUG" in log.method.upper():
                log_level = "DEBUG"
            
            # 构建日志数据
            log_data = {
                "id": f"LOG-{log.id}",
                "time": log.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "level": log_level,
                "module": log.method.split()[0] if log.method and " " in log.method else "system",
                "message": f"{log.method} {log.path}"
            }
            
            recent.append(log_data)
        
        # 如果没有足够的日志，添加一些模拟数据
        if len(recent) < 3:
            mock_recent = [
                {
                    "id": "LOG-050",
                    "time": (datetime.utcnow() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
                    "level": "ERROR",
                    "module": "notifications",
                    "message": "Provider timeout"
                },
                {
                    "id": "LOG-049",
                    "time": (datetime.utcnow() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
                    "level": "WARN",
                    "module": "auth",
                    "message": "Multiple failed login attempts"
                },
                {
                    "id": "LOG-048",
                    "time": (datetime.utcnow() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
                    "level": "INFO",
                    "module": "user",
                    "message": "User profile updated"
                }
            ]
            
            # 添加模拟数据直到有3条记录
            while len(recent) < 3:
                recent.append(mock_recent[3 - len(recent) - 1])
        
        # 获取模块统计
        # 这里我们模拟一些模块数据，实际应该从日志中提取
        top_modules = [
            {"module": "billing", "total": 9},
            {"module": "auth", "total": 7},
            {"module": "user", "total": 6},
            {"module": "notifications", "total": 5},
            {"module": "system", "total": 4}
        ]
        
        # 计算错误率
        error_ratio = 0.0
        if total_logs > 0:
            error_ratio = round((error_count / total_logs) * 100, 1)
        
        result = {
            "severity": severity,
            "recent": recent,
            "topModules": top_modules,
            "total": total_logs,
            "errorRatio": error_ratio
        }
        
        logger.info("获取日志概览数据成功")
        return result
        
    except Exception as e:
        logger.error(f"获取日志概览数据失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取日志概览数据失败"
        )

@router.get("/settings")
async def get_system_settings(db: Session = Depends(get_db)):
    """获取系统设置"""
    logger.info("获取系统设置")
    
    try:
        # 这里我们从环境变量或配置文件中读取设置
        # 由于没有专门的设置表，我们返回一些默认设置
        
        settings_data = {
            "appName": "Demo FastAPI Platform",
            "language": "zh",
            "timezone": "Asia/Shanghai",
            "theme": "light",
            "notifications": {
                "email": True,
                "sms": False,
                "inApp": True
            },
            "security": {
                "mfa": True,
                "sessionTimeout": 30,
                "passwordPolicy": "长度≥12，含数字和特殊字符"
            }
        }
        
        logger.info("获取系统设置成功")
        return settings_data
        
    except Exception as e:
        logger.error(f"获取系统设置失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取系统设置失败"
        )

@router.put("/settings")
async def update_system_settings(
    settings_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """更新系统设置"""
    logger.info("更新系统设置")
    
    try:
        # 在实际应用中，这里应该更新数据库或配置文件中的设置
        # 由于没有专门的设置表，这里只是模拟操作
        
        # 验证设置数据
        required_fields = ["appName", "language", "timezone", "theme"]
        for field in required_fields:
            if field not in settings_data:
                raise HTTPException(
                    status_code=400,
                    detail=f"缺少必填字段: {field}"
                )
        
        # 验证嵌套对象
        if "notifications" not in settings_data:
            settings_data["notifications"] = {
                "email": True,
                "sms": False,
                "inApp": True
            }
        
        if "security" not in settings_data:
            settings_data["security"] = {
                "mfa": True,
                "sessionTimeout": 30,
                "passwordPolicy": "长度≥12，含数字和特殊字符"
            }
        
        logger.info("系统设置更新成功")
        
        # 返回更新后的设置
        return settings_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新系统设置失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="更新系统设置失败"
        )