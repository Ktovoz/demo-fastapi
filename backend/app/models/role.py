from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from typing import List, TYPE_CHECKING

from .base import BaseModel

# TYPE_CHECKING避免循环导入错误
if TYPE_CHECKING:
    from .user_role import UserRole
    from .role_permission import RolePermission

class Role(BaseModel):
    """角色模型"""
    __tablename__ = "roles"

    name = Column(String(50), unique=True, index=True, nullable=False, comment="角色名称")
    description = Column(String(200), comment="角色描述")

    # 关系定义
    user_roles = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")
    role_permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Role(name='{self.name}', description='{self.description}')>"

    def get_users(self):
        """获取所有拥有此角色的用户"""
        if hasattr(self, '_cached_users'):
            return self._cached_users
        return []

    def get_permissions(self):
        """获取角色所有权限"""
        if hasattr(self, '_cached_permissions'):
            return self._cached_permissions
        return []