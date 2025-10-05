from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

from .base import BaseModel

# TYPE_CHECKING避免循环导入错误
if TYPE_CHECKING:
    from .user import User

class OperationLog(BaseModel):
    """操作日志模型"""
    __tablename__ = "operation_logs"
    
    # 添加索引以优化查询
    __table_args__ = (
        Index('idx_operation_log_user_id', 'user_id'),
        Index('idx_operation_log_action', 'action'),
        Index('idx_operation_log_resource', 'resource'),
        Index('idx_operation_log_ip_address', 'ip_address'),
        Index('idx_operation_log_created_at', 'created_at'),
    )

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    action = Column(String(50), nullable=False, comment="操作类型")
    resource = Column(String(50), nullable=False, comment="操作资源")
    resource_id = Column(Integer, comment="资源ID")
    description = Column(Text, comment="操作描述")
    ip_address = Column(String(45), comment="IP地址")
    user_agent = Column(String(255), comment="用户代理")
    request_data = Column(JSON, comment="请求数据")
    response_data = Column(JSON, comment="响应数据")

    # 关系
    user = relationship("User", back_populates="operation_logs")

    def __repr__(self):
        return f"<OperationLog(user_id={self.user_id}, action='{self.action}', resource='{self.resource}')>"