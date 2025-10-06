from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime

from ..models.role import Role
from ..models.user_role import UserRole
from ..models.role_permission import RolePermission
from ..models.permission import Permission
from ..utils.logger import get_logger
from ..utils.exceptions import ValidationError, NotFoundError, DatabaseError
from ..utils.cache import cache

logger = get_logger(__name__)

class RoleManagementService:
    """角色管理服务"""
    
    @staticmethod
    def get_roles_list(db: Session) -> List[Dict[str, Any]]:
        """获取角色列表"""
        try:
            # 尝试从缓存获取
            cache_key = "roles_list"
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug("从缓存获取角色列表")
                return cached_result
            
            # 查询所有角色
            roles = db.query(Role).all()
            
            # 构建返回数据
            result = []
            for role in roles:
                # 获取角色成员数量
                members_count = db.query(UserRole).filter(UserRole.role_id == role.id).count()
                
                # 获取角色权限
                permissions = []
                try:
                    for role_permission in role.role_permissions:
                        permissions.append(role_permission.permission.name)
                except Exception as e:
                    logger.warning(f"获取角色权限失败: {str(e)}")
                
                # 构建角色数据
                role_data = {
                    "id": f"ROLE-{role.id}",
                    "displayName": role.name,
                    "description": role.description or "",
                    "members": members_count,
                    "permissions": permissions,
                    "status": "active"  # 模拟数据，实际应从角色表获取
                }
                
                result.append(role_data)
            
            # 缓存结果（5分钟）
            cache.set(cache_key, result, ttl=300)
            
            return result
            
        except Exception as e:
            logger.error(f"获取角色列表失败: {str(e)}")
            raise DatabaseError(f"获取角色列表失败: {str(e)}")
    
    @staticmethod
    def get_role_detail(db: Session, role_id: str) -> Dict[str, Any]:
        """获取角色详情"""
        try:
            # 验证参数
            if not role_id:
                raise ValidationError("角色ID不能为空", "role_id")
            
            # 提取角色ID
            if role_id.startswith("ROLE-"):
                role_id = role_id[5:]
            
            # 验证角色ID格式
            try:
                role_id_int = int(role_id)
            except ValueError:
                raise ValidationError("角色ID格式不正确", "role_id")
            
            # 尝试从缓存获取
            cache_key = f"role_detail_{role_id}"
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"从缓存获取角色详情: {role_id}")
                return cached_result
            
            # 查询角色
            role = db.query(Role).filter(Role.id == role_id_int).first()
            if not role:
                raise NotFoundError("角色", role_id)
            
            # 获取角色权限
            permissions = []
            try:
                for role_permission in role.role_permissions:
                    permissions.append(role_permission.permission.name)
            except Exception as e:
                logger.warning(f"获取角色权限失败: {str(e)}")
            
            # 构建角色数据
            role_data = {
                "id": f"ROLE-{role.id}",
                "displayName": role.name,
                "description": role.description or "",
                "permissions": permissions,
                "status": "active"  # 模拟数据，实际应从角色表获取
            }
            
            # 缓存结果（5分钟）
            cache.set(cache_key, role_data, ttl=300)
            
            return role_data
            
        except ValidationError:
            raise
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"获取角色详情失败: {str(e)}")
            raise DatabaseError(f"获取角色详情失败: {str(e)}")
    
    @staticmethod
    def update_role(db: Session, role_id: str, role_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新角色信息"""
        try:
            # 验证参数
            if not role_id:
                raise ValidationError("角色ID不能为空", "role_id")
            
            # 提取角色ID
            if role_id.startswith("ROLE-"):
                role_id = role_id[5:]
            
            # 验证角色ID格式
            try:
                role_id_int = int(role_id)
            except ValueError:
                raise ValidationError("角色ID格式不正确", "role_id")
            
            # 查询角色
            role = db.query(Role).filter(Role.id == role_id_int).first()
            if not role:
                raise NotFoundError("角色", role_id)
            
            # 更新基本信息
            if "displayName" in role_data:
                if not role_data["displayName"]:
                    raise ValidationError("角色名称不能为空", "displayName")
                role.name = role_data["displayName"]
            
            if "description" in role_data:
                role.description = role_data["description"]
            
            # 更新最后修改时间
            role.updated_at = datetime.utcnow()
            db.commit()
            
            # 更新权限关联
            if "permissions" in role_data:
                # 删除现有权限关联
                db.query(RolePermission).filter(RolePermission.role_id == role.id).delete()
                
                # 添加新权限关联
                permissions = role_data["permissions"]
                if permissions:
                    for permission_name in permissions:
                        permission = db.query(Permission).filter(Permission.name == permission_name).first()
                        if permission:
                            role_permission = RolePermission(role_id=role.id, permission_id=permission.id)
                            db.add(role_permission)
                
                db.commit()
            
            # 清除相关缓存
            cache.delete(f"role_detail_{role_id}")
            cache.delete("roles_list")
            
            # 返回更新后的角色数据
            return RoleManagementService.get_role_detail(db, f"ROLE-{role.id}")
            
        except ValidationError:
            raise
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"更新角色信息失败: {str(e)}")
            db.rollback()
            raise DatabaseError(f"更新角色信息失败: {str(e)}")