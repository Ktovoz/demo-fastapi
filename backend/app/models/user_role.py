from sqlalchemy import Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship

from .base import BaseModel

class UserRole(BaseModel):
    """用户角色关联表"""
    __tablename__ = "user_roles"
    
    # 添加复合索引以优化查询
    __table_args__ = (
        Index('idx_user_role_user_id', 'user_id'),
        Index('idx_user_role_role_id', 'role_id'),
        Index('idx_user_role_user_role', 'user_id', 'role_id', unique=True),
    )

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, comment="角色ID")

    # 关系
    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")

    def __repr__(self):
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id})>"