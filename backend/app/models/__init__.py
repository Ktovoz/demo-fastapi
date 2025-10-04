# 数据模型模块 - 统一导入所有模型以避免循环依赖

# 首先导入基础模型
from .base import BaseModel

# 然后导入独立的模型（按顺序）
from .permission import Permission
from .role import Role
from .user_role import UserRole
from .role_permission import RolePermission
from .user import User
from .operation_log import OperationLog

# 最后导入所有模型到 __all__ 列表
__all__ = [
    "BaseModel",
    "Permission", 
    "Role",
    "UserRole",
    "RolePermission",
    "User",
    "OperationLog"
]