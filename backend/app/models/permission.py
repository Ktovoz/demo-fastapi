from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from typing import List, TYPE_CHECKING

from .base import BaseModel

# TYPE_CHECKING避免循环导入错误
if TYPE_CHECKING:
    from .role_permission import RolePermission

class Permission(BaseModel):
    """权限模型"""
    __tablename__ = "permissions"

    name = Column(String(100), unique=True, index=True, nullable=False, comment="权限名称")
    resource = Column(String(50), nullable=False, comment="资源名称")
    action = Column(String(50), nullable=False, comment="操作类型")
    description = Column(String(200), comment="权限描述")

    # 关系定义
    role_permissions = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Permission(name='{self.name}', resource='{self.resource}', action='{self.action}')>"

    def get_roles(self):
        """获取拥有此权限的所有角色"""
        if hasattr(self, '_cached_roles'):
            return self._cached_roles
        return []