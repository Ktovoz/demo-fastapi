from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..models.user import User
from ..routers.auth import get_current_user
from ..utils.logger import get_logger

logger = get_logger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login-json")

def require_permissions(required_permissions: List[str]):
    """权限校验装饰器工厂"""
    def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        """检查用户是否有所需权限"""
        logger.debug(f"检查用户权限: {current_user.username}, 需要权限: {required_permissions}")
        
        # 超级用户拥有所有权限
        if current_user.is_superuser:
            logger.debug(f"用户 {current_user.username} 是超级用户，跳过权限检查")
            return current_user
        
        # 获取用户所有权限
        user_permissions = []
        try:
            for user_role in current_user.user_roles:
                for role_permission in user_role.role.role_permissions:
                    user_permissions.append(role_permission.permission.name)
            user_permissions = list(set(user_permissions))
        except Exception as e:
            logger.error(f"获取用户权限失败: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="获取用户权限失败"
            )
        
        # 检查是否有所需权限
        has_permission = False
        for permission in required_permissions:
            if permission in user_permissions or "*" in user_permissions:
                has_permission = True
                break
        
        if not has_permission:
            logger.warning(f"用户 {current_user.username} 权限不足，需要权限: {required_permissions}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )
        
        logger.debug(f"用户 {current_user.username} 权限检查通过")
        return current_user
    
    return permission_checker

def require_roles(required_roles: List[str]):
    """角色校验装饰器工厂"""
    def role_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        """检查用户是否有所需角色"""
        logger.debug(f"检查用户角色: {current_user.username}, 需要角色: {required_roles}")
        
        # 超级用户拥有所有角色
        if current_user.is_superuser:
            logger.debug(f"用户 {current_user.username} 是超级用户，跳过角色检查")
            return current_user
        
        # 获取用户所有角色
        user_roles = []
        try:
            for user_role in current_user.user_roles:
                user_roles.append(user_role.role.name)
        except Exception as e:
            logger.error(f"获取用户角色失败: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="获取用户角色失败"
            )
        
        # 检查是否有所需角色
        has_role = any(role in user_roles for role in required_roles)
        
        if not has_role:
            logger.warning(f"用户 {current_user.username} 角色不足，需要角色: {required_roles}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="角色不足"
            )
        
        logger.debug(f"用户 {current_user.username} 角色检查通过")
        return current_user
    
    return role_checker

# 常用权限校验器
require_admin = require_roles(["admin"])
require_user_management = require_permissions(["users:view", "users:edit", "users:delete"])
require_role_management = require_permissions(["roles:view", "roles:edit"])
require_system_management = require_permissions(["system:view", "system:edit"])
require_audit_view = require_permissions(["audit:view"])

# 可选的权限校验器（不强制要求）
def optional_permission_checker(
    required_permissions: List[str],
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """可选的权限校验，不抛出异常，返回是否有权限的标志"""
    if not current_user:
        return {"user": None, "has_permission": False}
    
    # 超级用户拥有所有权限
    if current_user.is_superuser:
        return {"user": current_user, "has_permission": True}
    
    # 获取用户所有权限
    user_permissions = []
    try:
        for user_role in current_user.user_roles:
            for role_permission in user_role.role.role_permissions:
                user_permissions.append(role_permission.permission.name)
        user_permissions = list(set(user_permissions))
    except Exception as e:
        logger.error(f"获取用户权限失败: {str(e)}")
        return {"user": current_user, "has_permission": False}
    
    # 检查是否有所需权限
    has_permission = any(
        permission in user_permissions or "*" in user_permissions 
        for permission in required_permissions
    )
    
    return {"user": current_user, "has_permission": has_permission}