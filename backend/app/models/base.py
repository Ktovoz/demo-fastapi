from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from typing import Any, Dict
from ..core.database import Base

class BaseModel(Base):
    """基础模型类"""
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    is_active = Column(Boolean, default=True, comment="是否启用")

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """从字典更新属性"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)