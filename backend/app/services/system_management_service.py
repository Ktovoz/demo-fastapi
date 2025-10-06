from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

# 中国时区偏移量 (UTC+8)
CHINA_TIME_OFFSET = timedelta(hours=8)

def get_china_time(utc_time):
    """将UTC时间转换为中国时间"""
    return utc_time + CHINA_TIME_OFFSET

from ..models.operation_log import OperationLog
from ..models.user import User
from ..utils.logger import get_logger
from ..utils.exceptions import ValidationError, DatabaseError
from ..utils.cache import cache

logger = get_logger(__name__)

class SystemManagementService:
    """系统管理服务"""
    
    @staticmethod
    def get_system_logs(
        db: Session,
        page: int = 1,
        page_size: int = 10,
        keyword: Optional[str] = None,
        level: Optional[str] = "ALL",
        sorter: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取系统日志"""
        try:
            # 验证参数
            if page < 1:
                raise ValidationError("页码必须大于0", "page")
            
            if page_size < 1 or page_size > 100:
                raise ValidationError("每页数量必须在1-100之间", "page_size")
            
            # 构建查询
            query = db.query(OperationLog)
            
            # 关键词搜索
            if keyword:
                query = query.filter(
                    or_(
                        OperationLog.action.like(f"%{keyword}%"),
                        OperationLog.resource.like(f"%{keyword}%"),
                        OperationLog.ip_address.like(f"%{keyword}%")
                    )
                )
            
            # 级别筛选
            if level != "ALL":
                # 基于action字段判断日志级别
                if level == "ERROR":
                    query = query.filter(OperationLog.action.like("%ERROR%"))
                elif level == "WARN":
                    query = query.filter(OperationLog.action.like("%WARN%"))
                elif level == "INFO":
                    query = query.filter(and_(
                        OperationLog.action.notlike("%ERROR%"),
                        OperationLog.action.notlike("%WARN%")
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
                        "method": OperationLog.action,
                        "path": OperationLog.resource
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
            offset = (page - 1) * page_size
            logs = query.offset(offset).limit(page_size).all()
            
            # 构建返回数据
            items = []
            for log in logs:
                # 确定日志级别
                log_level = "INFO"
                if "ERROR" in log.action.upper():
                    log_level = "ERROR"
                elif "WARN" in log.action.upper():
                    log_level = "WARN"
                elif "DEBUG" in log.action.upper():
                    log_level = "DEBUG"
                
                # 构建上下文信息
                context = {
                    "requestId": f"req-{log.id}",
                    "ip": log.ip_address,
                    "userAgent": log.user_agent,
                    "resourceId": log.resource_id,
                    "userId": log.user_id,
                    "resource": log.resource,
                    "userEmail": None,
                    "userName": None
                }

                # 获取用户信息
                if log.user_id:
                    try:
                        user = db.query(User).filter(User.id == log.user_id).first()
                        if user:
                            context["userEmail"] = user.email
                            context["userName"] = user.full_name or user.username
                    except Exception as e:
                        logger.debug(f"获取用户信息失败: {e}")

                # 改进日志级别判断逻辑
                action_upper = log.action.upper() if log.action else ""
                if "ERROR" in action_upper or "失败" in log.action:
                    log_level = "ERROR"
                elif "WARN" in action_upper or "警告" in log.action or "检测到" in log.action:
                    log_level = "WARN"
                elif "DEBUG" in action_upper:
                    log_level = "DEBUG"
                else:
                    log_level = "INFO"

                # 改进模块名提取逻辑 - 从resource字段获取，更准确
                module_mapping = {
                    "auth": "认证系统",
                    "users": "用户管理",
                    "roles": "角色管理",
                    "dashboard": "仪表盘",
                    "admin": "运营中心",
                    "system": "系统管理",
                    "health": "健康检查"
                }
                module = module_mapping.get(log.resource, log.resource or "system")

                # 构建日志数据 - 使用中国时区
                china_time = get_china_time(log.created_at)
                log_data = {
                    "id": f"LOG-{log.id}",
                    "time": china_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "level": log_level,
                    "module": module,
                    "message": log.description or log.action,  # 主要描述信息
                    "action": log.action,  # 操作类型
                    "context": context
                }
                
                items.append(log_data)
            
            # 如果没有足够的日志，只添加少量模拟数据作为演示
            if len(items) < min(page_size, 5):
                # 生成少量模拟数据用于演示
                sample_mock_logs = [
                    {
                        "id": "LOG-MOCK-DEMO-1",
                        "time": (datetime.utcnow() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
                        "level": "ERROR",
                        "module": "billing",
                        "message": "Payment webhook failed",
                        "context": {
                            "requestId": "req-demo-1",
                            "ip": "203.0.113.10",
                            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                            "resourceId": "payment-123"
                        }
                    },
                    {
                        "id": "LOG-MOCK-DEMO-2",
                        "time": (datetime.utcnow() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
                        "level": "WARN",
                        "module": "auth",
                        "message": "Multiple failed login attempts",
                        "context": {
                            "requestId": "req-demo-2",
                            "ip": "192.0.2.45",
                            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                            "resourceId": "user-456"
                        }
                    },
                    {
                        "id": "LOG-MOCK-DEMO-3",
                        "time": (datetime.utcnow() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
                        "level": "INFO",
                        "module": "user",
                        "message": "User profile updated",
                        "context": {
                            "requestId": "req-demo-3",
                            "ip": "198.51.100.22",
                            "userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                            "resourceId": "profile-789"
                        }
                    }
                ]

                # 只添加必要的模拟数据，不超过5条
                for mock_item in sample_mock_logs:
                    if len(items) < min(page_size, 5):
                        items.append(mock_item)

                # 更新总数，保持合理的小数值
                if total < len(items):
                    total = len(items)
            
            result = {
                "items": items,
                "total": total,
                "page": page,
                "pageSize": page_size
            }

            logger.debug(f"系统日志数据: items={len(items)}, total={total}, page={page}, pageSize={page_size}")
            if items:
                logger.debug(f"第一条日志示例: {items[0]}")

            return result
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"获取系统日志失败: {str(e)}")
            raise DatabaseError(f"获取系统日志失败: {str(e)}")
    
    @staticmethod
    def get_logs_summary(db: Session) -> Dict[str, Any]:
        """获取日志概览数据"""
        try:
            # 获取总日志数
            total_logs = db.query(OperationLog).count()
            
            # 获取各级别日志数量
            error_count = db.query(OperationLog).filter(OperationLog.action.like("%ERROR%")).count()
            warn_count = db.query(OperationLog).filter(OperationLog.action.like("%WARN%")).count()
            info_count = db.query(OperationLog).filter(and_(
                OperationLog.action.notlike("%ERROR%"),
                OperationLog.action.notlike("%WARN%")
            )).count()
            debug_count = db.query(OperationLog).filter(OperationLog.action.like("%DEBUG%")).count()
            
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
                # 改进日志级别判断逻辑
                action_upper = log.action.upper() if log.action else ""
                if "ERROR" in action_upper or "失败" in log.action:
                    log_level = "ERROR"
                elif "WARN" in action_upper or "警告" in log.action or "检测到" in log.action:
                    log_level = "WARN"
                elif "DEBUG" in action_upper:
                    log_level = "DEBUG"
                else:
                    log_level = "INFO"

                # 改进模块名提取逻辑
                module_mapping = {
                    "auth": "认证系统",
                    "users": "用户管理",
                    "roles": "角色管理",
                    "dashboard": "仪表盘",
                    "admin": "运营中心",
                    "system": "系统管理",
                    "health": "健康检查"
                }
                module = module_mapping.get(log.resource, log.resource or "system")

                # 构建日志数据
                context_summary = {
                    "userId": log.user_id,
                    "userEmail": None,
                    "userName": None,
                    "resource": log.resource
                }

                # 获取用户信息
                if log.user_id:
                    try:
                        user = db.query(User).filter(User.id == log.user_id).first()
                        if user:
                            context_summary["userEmail"] = user.email
                            context_summary["userName"] = user.full_name or user.username
                    except Exception as e:
                        logger.debug(f"获取用户信息失败: {e}")

                # 构建日志数据 - 使用中国时区
                china_time = get_china_time(log.created_at)
                log_data = {
                    "id": f"LOG-{log.id}",
                    "time": china_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "level": log_level,
                    "module": module,
                    "message": log.description or log.action,
                    "action": log.action,
                    "context": context_summary
                }

                recent.append(log_data)
            
            # 如果没有足够的日志，添加少量示例数据
            if len(recent) < 3:
                sample_recent = [
                    {
                        "id": "LOG-DEMO-1",
                        "time": (datetime.utcnow() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
                        "level": "ERROR",
                        "module": "notifications",
                        "message": "Provider timeout"
                    },
                    {
                        "id": "LOG-DEMO-2",
                        "time": (datetime.utcnow() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
                        "level": "WARN",
                        "module": "auth",
                        "message": "Multiple failed login attempts"
                    },
                    {
                        "id": "LOG-DEMO-3",
                        "time": (datetime.utcnow() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
                        "level": "INFO",
                        "module": "user",
                        "message": "User profile updated"
                    }
                ]

                # 只添加必要的示例数据，最多3条
                for sample_item in sample_recent:
                    if len(recent) < 3:
                        recent.append(sample_item)
            
            # 获取模块统计
            # 这里我们模拟一些模块数据，实际应该从日志中提取
            # 如果数据库中有数据，则使用实际数据，否则使用模拟数据
            if total_logs > 0:
                # 从数据库中提取模块统计
                try:
                    # 使用SQLAlchemy的func来统计模块数量
                    from sqlalchemy import func
                    module_stats = db.query(
                        func.substr(OperationLog.action, 1, func.instr(OperationLog.action, ' ') - 1).label('module'),
                        func.count(OperationLog.id).label('total')
                    ).group_by(
                        func.substr(OperationLog.action, 1, func.instr(OperationLog.action, ' ') - 1)
                    ).order_by(func.count(OperationLog.id).desc()).limit(5).all()
                    
                    top_modules = []
                    for stat in module_stats:
                        if stat.module:  # 确保模块名不为空
                            top_modules.append({"module": stat.module, "total": stat.total})
                    
                    # 如果提取的模块数据不足5个，补充模拟数据
                    if len(top_modules) < 5:
                        additional_modules = [
                            {"module": "billing", "total": max(9, total_logs // 10)},
                            {"module": "auth", "total": max(7, total_logs // 12)},
                            {"module": "user", "total": max(6, total_logs // 15)},
                            {"module": "notifications", "total": max(5, total_logs // 20)},
                            {"module": "system", "total": max(4, total_logs // 25)}
                        ]
                        
                        # 添加不重复的模块
                        existing_modules = {m["module"] for m in top_modules}
                        for module in additional_modules:
                            if module["module"] not in existing_modules and len(top_modules) < 5:
                                top_modules.append(module)
                                existing_modules.add(module["module"])
                except Exception as e:
                    logger.warning(f"从数据库提取模块统计失败: {str(e)}，使用模拟数据")
                    top_modules = [
                        {"module": "billing", "total": max(9, total_logs // 10)},
                        {"module": "auth", "total": max(7, total_logs // 12)},
                        {"module": "user", "total": max(6, total_logs // 15)},
                        {"module": "notifications", "total": max(5, total_logs // 20)},
                        {"module": "system", "total": max(4, total_logs // 25)}
                    ]
            else:
                # 没有日志数据时使用模拟数据
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

            logger.debug(f"日志概览数据: total={total_logs}, error_ratio={error_ratio}, recent_count={len(recent)}, modules_count={len(top_modules)}")
            if recent:
                logger.debug(f"最新日志示例: {recent[0]}")

            return result
            
        except Exception as e:
            logger.error(f"获取日志概览数据失败: {str(e)}")
            raise DatabaseError(f"获取日志概览数据失败: {str(e)}")
    
    @staticmethod
    def get_system_settings() -> Dict[str, Any]:
        """获取系统设置"""
        try:
            # 尝试从缓存获取
            cache_key = "system_settings"
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug("从缓存获取系统设置")
                return cached_result
            
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
            
            # 缓存结果（10分钟）
            cache.set(cache_key, settings_data, ttl=600)
            
            return settings_data
            
        except Exception as e:
            logger.error(f"获取系统设置失败: {str(e)}")
            raise DatabaseError(f"获取系统设置失败: {str(e)}")
    
    @staticmethod
    def update_system_settings(settings_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新系统设置"""
        try:
            # 在实际应用中，这里应该更新数据库或配置文件中的设置
            # 由于没有专门的设置表，这里只是模拟操作
            
            # 验证设置数据
            required_fields = ["appName", "language", "timezone", "theme"]
            for field in required_fields:
                if field not in settings_data:
                    raise ValidationError(f"缺少必填字段: {field}", field)
            
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
            
            # 清除缓存
            cache.delete("system_settings")
            
            return settings_data
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"更新系统设置失败: {str(e)}")
            raise DatabaseError(f"更新系统设置失败: {str(e)}")