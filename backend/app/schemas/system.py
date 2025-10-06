from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class LogEntry(BaseModel):
    """日志条目模型"""
    id: str = Field(..., description="日志ID")
    time: str = Field(..., description="时间")
    level: str = Field(..., description="日志级别")
    module: str = Field(..., description="模块")
    message: str = Field(..., description="消息")
    context: Optional[Dict[str, Any]] = Field(None, description="上下文信息")

class LogSeverity(BaseModel):
    """日志严重程度模型"""
    ERROR: int = Field(..., description="错误数量")
    WARN: int = Field(..., description="警告数量")
    INFO: int = Field(..., description="信息数量")
    DEBUG: int = Field(..., description="调试数量")

class LogSummaryResponse(BaseModel):
    """日志概览响应模型"""
    severity: LogSeverity = Field(..., description="严重程度统计")
    recent: List[LogEntry] = Field(..., description="最近日志")
    topModules: List[Dict[str, Any]] = Field(..., description="顶级模块")
    total: int = Field(..., description="总日志数")
    errorRatio: float = Field(..., description="错误率")

class LogListResponse(BaseModel):
    """日志列表响应模型"""
    items: List[LogEntry] = Field(..., description="日志列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    pageSize: int = Field(..., description="每页数量")

class NotificationSettings(BaseModel):
    """通知设置模型"""
    email: bool = Field(True, description="邮件通知")
    sms: bool = Field(False, description="短信通知")
    inApp: bool = Field(True, description="应用内通知")

class SecuritySettings(BaseModel):
    """安全设置模型"""
    mfa: bool = Field(True, description="多因素认证")
    sessionTimeout: int = Field(30, description="会话超时时间(分钟)")
    passwordPolicy: str = Field("长度≥12，含数字和特殊字符", description="密码策略")

class SystemSettings(BaseModel):
    """系统设置模型"""
    appName: str = Field(..., description="应用名称")
    language: str = Field(..., description="语言")
    timezone: str = Field(..., description="时区")
    theme: str = Field(..., description="主题")
    notifications: NotificationSettings = Field(..., description="通知设置")
    security: SecuritySettings = Field(..., description="安全设置")

class SystemSettingsUpdate(BaseModel):
    """系统设置更新模型"""
    appName: str = Field(..., description="应用名称")
    language: str = Field(..., description="语言")
    timezone: str = Field(..., description="时区")
    theme: str = Field(..., description="主题")
    notifications: Optional[NotificationSettings] = Field(None, description="通知设置")
    security: Optional[SecuritySettings] = Field(None, description="安全设置")