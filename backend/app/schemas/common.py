from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class HealthCheckResponse(BaseModel):
    """健康检查响应模式"""
    status: str = Field(..., description="服务状态")
    message: str = Field(..., description="状态消息")
    version: str = Field(..., description="应用版本")
    timestamp: datetime = Field(..., description="检查时间")
    database_status: Optional[str] = Field(None, description="数据库状态")

class SuccessResponse(BaseModel):
    """成功响应模式"""
    message: str = Field(..., description="操作结果消息")
    status_code: int = Field(default=200, description="状态码")

class ErrorResponse(BaseModel):
    """错误响应模式"""
    error: str = Field(..., description="错误类型")
    message: str = Field(..., description="错误消息")
    status_code: int = Field(..., description="状态码")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="错误时间")