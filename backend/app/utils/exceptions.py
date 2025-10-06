from fastapi import HTTPException, status
from typing import Optional, Dict, Any

class ServiceError(Exception):
    """服务层异常基类"""
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        self.message = message
        self.error_code = error_code or "SERVICE_ERROR"
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(ServiceError):
    """验证错误"""
    def __init__(self, message: str, field: str = None, details: Dict[str, Any] = None):
        super().__init__(message, "VALIDATION_ERROR", details)
        self.field = field

class NotFoundError(ServiceError):
    """资源未找到错误"""
    def __init__(self, resource: str, resource_id: str = None, details: Dict[str, Any] = None):
        message = f"{resource}未找到"
        if resource_id:
            message = f"{resource}未找到: {resource_id}"
        super().__init__(message, "NOT_FOUND", details)
        self.resource = resource
        self.resource_id = resource_id

class ConflictError(ServiceError):
    """资源冲突错误"""
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "CONFLICT", details)

class DatabaseError(ServiceError):
    """数据库错误"""
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "DATABASE_ERROR", details)

def service_exception_handler(exc: ServiceError) -> HTTPException:
    """将服务层异常转换为HTTP异常"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    if isinstance(exc, ValidationError):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exc, NotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, ConflictError):
        status_code = status.HTTP_409_CONFLICT
    elif isinstance(exc, DatabaseError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    return HTTPException(
        status_code=status_code,
        detail={
            "message": exc.message,
            "error_code": exc.error_code,
            "details": exc.details
        }
    )