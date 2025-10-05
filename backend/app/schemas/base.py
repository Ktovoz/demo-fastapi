from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, Any, Dict
from datetime import datetime

T = TypeVar('T')

class BaseResponse(BaseModel):
    """基础响应模型"""
    success: bool = True
    message: str = ""
    data: Optional[Any] = None
    error_code: Optional[str] = None
    timestamp: datetime = datetime.utcnow()
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }

class PaginatedResponse(BaseModel):
    """分页响应模型"""
    success: bool = True
    message: str = ""
    data: Dict[str, Any] = {}
    error_code: Optional[str] = None
    timestamp: datetime = datetime.utcnow()
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }