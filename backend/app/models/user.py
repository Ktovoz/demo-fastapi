from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List, TYPE_CHECKING

from .base import BaseModel

# TYPE_CHECKING避免循环导入错误
if TYPE_CHECKING:
    from .user_role import UserRole
    from .operation_log import OperationLog

class User(BaseModel):
    """用户模型"""
    __tablename__ = "users"

    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    full_name = Column(String(100), comment="全名")
    avatar = Column(String(255), comment="头像URL")
    is_superuser = Column(Boolean, default=False, comment="是否超级用户")
    last_login = Column(DateTime(timezone=True), comment="最后登录时间")

    # 关系定义
    user_roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    operation_logs = relationship("OperationLog", back_populates="user")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

    def get_roles(self):
        """获取用户所有角色"""
        if hasattr(self, '_cached_roles'):
            return self._cached_roles
        return []

    def get_permissions(self):
        """获取用户所有权限"""
        if hasattr(self, '_cached_permissions'):
            return self._cached_permissions
        return []

    def has_role(self, role_name: str) -> bool:
        """检查用户是否有指定角色"""
        return any(role.name == role_name for role in self.get_roles())

    def has_permission(self, permission_name: str) -> bool:
        """检查用户是否有指定权限"""
        return any(permission.name == permission_name for permission in self.get_permissions())