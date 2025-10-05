from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json

from ..models.user import User
from ..models.user_role import UserRole
from ..models.role import Role
from ..core.security import get_password_hash
from ..utils.logger import get_logger
from ..utils.exceptions import ValidationError, NotFoundError, ConflictError, DatabaseError

logger = get_logger(__name__)

class UserManagementService:
    """用户管理服务"""
    
    @staticmethod
    def get_users_list(
        db: Session,
        page: int = 1,
        page_size: int = 10,
        keyword: Optional[str] = None,
        status: Optional[str] = "all",
        role: Optional[str] = "all",
        sorter: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取用户列表"""
        try:
            # 验证参数
            if page < 1:
                raise ValidationError("页码必须大于0", "page")
            
            if page_size < 1 or page_size > 100:
                raise ValidationError("每页数量必须在1-100之间", "page_size")
            
            # 构建查询
            query = db.query(User)
            
            # 关键词搜索
            if keyword:
                query = query.filter(
                    or_(
                        User.full_name.like(f"%{keyword}%"),
                        User.email.like(f"%{keyword}%"),
                        User.username.like(f"%{keyword}%")
                    )
                )
            
            # 角色筛选
            if role != "all":
                query = query.join(UserRole).join(Role).filter(Role.name == role)
            
            # 排序处理
            if sorter:
                try:
                    sorter_data = json.loads(sorter) if isinstance(sorter, str) else sorter
                    field = sorter_data.get("field", "id")
                    order = sorter_data.get("order", "ascend")
                    
                    # 映射字段名
                    field_mapping = {
                        "name": User.full_name,
                        "email": User.email,
                        "lastLogin": User.last_login,
                        "createdAt": User.created_at
                    }
                    
                    if field in field_mapping:
                        if order == "descend":
                            query = query.order_by(field_mapping[field].desc())
                        else:
                            query = query.order_by(field_mapping[field].asc())
                except Exception as e:
                    logger.warning(f"排序参数解析失败: {str(e)}")
                    # 使用默认排序
                    query = query.order_by(User.id)
            else:
                # 默认排序
                query = query.order_by(User.id)
            
            # 计算总数
            total = query.count()
            
            # 分页
            offset = (page - 1) * page_size
            users = query.offset(offset).limit(page_size).all()
            
            # 构建返回数据
            items = []
            for user in users:
                # 获取用户角色和权限
                user_roles, user_permissions = UserManagementService._get_user_roles_and_permissions(user)
                
                # 构建用户数据
                user_data = {
                    "id": f"USR-{user.id}",
                    "name": user.full_name or user.username,
                    "email": user.email,
                    "role": user_roles[0] if user_roles else "user",
                    "roleName": user_roles[0] if user_roles else "普通用户",
                    "department": "技术部",  # 模拟数据，实际应从用户表获取
                    "status": "active",  # 模拟数据，实际应从用户表获取
                    "lastLogin": user.last_login.isoformat() + "Z" if user.last_login else None,
                    "avatar": user.avatar,
                    "tags": ["北京"],  # 模拟数据，实际应从用户表获取
                    "permissions": user_permissions[:5]  # 只显示前5个权限
                }
                
                items.append(user_data)
            
            result = {
                "items": items,
                "total": total,
                "page": page,
                "pageSize": page_size
            }
            
            return result
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"获取用户列表失败: {str(e)}")
            raise DatabaseError(f"获取用户列表失败: {str(e)}")
    
    @staticmethod
    def get_user_detail(db: Session, user_id: str) -> Dict[str, Any]:
        """获取用户详情"""
        try:
            # 验证参数
            if not user_id:
                raise ValidationError("用户ID不能为空", "user_id")
            
            # 提取用户ID
            if user_id.startswith("USR-"):
                user_id = user_id[4:]
            
            # 验证用户ID格式
            try:
                user_id_int = int(user_id)
            except ValueError:
                raise ValidationError("用户ID格式不正确", "user_id")
            
            # 查询用户
            user = db.query(User).filter(User.id == user_id_int).first()
            if not user:
                raise NotFoundError("用户", user_id)
            
            # 获取用户角色和权限
            user_roles, user_permissions = UserManagementService._get_user_roles_and_permissions(user)
            
            # 构建用户数据
            user_data = {
                "id": f"USR-{user.id}",
                "name": user.full_name or user.username,
                "email": user.email,
                "role": user_roles[0] if user_roles else "user",
                "roleName": user_roles[0] if user_roles else "普通用户",
                "status": "active",  # 模拟数据，实际应从用户表获取
                "department": "技术部",  # 模拟数据，实际应从用户表获取
                "phone": "+86-13800138000",  # 模拟数据，实际应从用户表获取
                "tags": ["北京", "前端"],  # 模拟数据，实际应从用户表获取
                "permissions": user_permissions,
                "avatar": user.avatar,
                "is_superuser": user.is_superuser,  # 添加超级用户标识
                "createdAt": user.created_at.isoformat() + "Z" if user.created_at else None,
                "lastLogin": user.last_login.isoformat() + "Z" if user.last_login else None
            }
            
            return user_data
            
        except ValidationError:
            raise
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"获取用户详情失败: {str(e)}")
            raise DatabaseError(f"获取用户详情失败: {str(e)}")
    
    @staticmethod
    def create_user(db: Session, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建用户"""
        try:
            # 验证必填字段
            required_fields = ["name", "email", "password"]
            for field in required_fields:
                if field not in user_data or not user_data[field]:
                    raise ValidationError(f"字段 {field} 不能为空", field)
            
            # 验证邮箱格式
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, user_data["email"]):
                raise ValidationError("邮箱格式不正确", "email")
            
            # 检查邮箱是否已存在
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if existing_user:
                raise ConflictError("邮箱已被注册")
            
            # 生成用户名
            username = user_data["email"].split("@")[0]
            existing_username = db.query(User).filter(User.username == username).first()
            if existing_username:
                import random
                username = f"{username}{random.randint(1000, 9999)}"
            
            # 创建用户
            hashed_password = get_password_hash(user_data["password"])
            new_user = User(
                username=username,
                email=user_data["email"],
                password_hash=hashed_password,
                full_name=user_data["name"],
                avatar=user_data.get("avatar")
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            # 如果指定了角色，添加角色关联
            if "role" in user_data and user_data["role"]:
                role = db.query(Role).filter(Role.name == user_data["role"]).first()
                if role:
                    user_role = UserRole(user_id=new_user.id, role_id=role.id)
                    db.add(user_role)
                    db.commit()
            
            # 返回创建的用户数据
            return UserManagementService.get_user_detail(db, f"USR-{new_user.id}")
            
        except ValidationError:
            raise
        except ConflictError:
            raise
        except Exception as e:
            logger.error(f"创建用户失败: {str(e)}")
            db.rollback()
            raise DatabaseError(f"创建用户失败: {str(e)}")
    
    @staticmethod
    def update_user(db: Session, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新用户信息"""
        try:
            # 验证参数
            if not user_id:
                raise ValidationError("用户ID不能为空", "user_id")
            
            # 提取用户ID
            if user_id.startswith("USR-"):
                user_id = user_id[4:]
            
            # 验证用户ID格式
            try:
                user_id_int = int(user_id)
            except ValueError:
                raise ValidationError("用户ID格式不正确", "user_id")
            
            # 查询用户
            user = db.query(User).filter(User.id == user_id_int).first()
            if not user:
                raise NotFoundError("用户", user_id)
            
            # 更新基本信息
            if "name" in user_data:
                if not user_data["name"]:
                    raise ValidationError("姓名不能为空", "name")
                user.full_name = user_data["name"]
            
            if "email" in user_data and user_data["email"] != user.email:
                if not user_data["email"]:
                    raise ValidationError("邮箱不能为空", "email")
                
                # 验证邮箱格式
                import re
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, user_data["email"]):
                    raise ValidationError("邮箱格式不正确", "email")
                
                # 检查邮箱是否已被其他用户使用
                existing_user = db.query(User).filter(
                    and_(User.email == user_data["email"], User.id != user_id_int)
                ).first()
                if existing_user:
                    raise ConflictError("邮箱已被其他用户使用")
                user.email = user_data["email"]
            
            if "avatar" in user_data:
                user.avatar = user_data["avatar"]
            
            # 如果提供了密码，更新密码
            if "password" in user_data and user_data["password"]:
                if len(user_data["password"]) < 6:
                    raise ValidationError("密码长度不能少于6位", "password")
                user.password_hash = get_password_hash(user_data["password"])
            
            db.commit()
            
            # 更新角色关联
            if "role" in user_data:
                # 删除现有角色关联
                db.query(UserRole).filter(UserRole.user_id == user.id).delete()
                
                # 添加新角色关联
                if user_data["role"]:
                    role = db.query(Role).filter(Role.name == user_data["role"]).first()
                    if role:
                        user_role = UserRole(user_id=user.id, role_id=role.id)
                        db.add(user_role)
                
                db.commit()
            
            # 返回更新后的用户数据
            return UserManagementService.get_user_detail(db, f"USR-{user.id}")
            
        except ValidationError:
            raise
        except NotFoundError:
            raise
        except ConflictError:
            raise
        except Exception as e:
            logger.error(f"更新用户信息失败: {str(e)}")
            db.rollback()
            raise DatabaseError(f"更新用户信息失败: {str(e)}")
    
    @staticmethod
    def update_user_status(db: Session, user_id: str, status_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新用户状态"""
        try:
            # 验证参数
            if not user_id:
                raise ValidationError("用户ID不能为空", "user_id")
            
            # 提取用户ID
            if user_id.startswith("USR-"):
                user_id = user_id[4:]
            
            # 验证用户ID格式
            try:
                user_id_int = int(user_id)
            except ValueError:
                raise ValidationError("用户ID格式不正确", "user_id")
            
            # 查询用户
            user = db.query(User).filter(User.id == user_id_int).first()
            if not user:
                raise NotFoundError("用户", user_id)
            
            # 更新最后修改时间
            user.updated_at = datetime.utcnow()
            db.commit()
            
            return {
                "id": f"USR-{user.id}",
                "status": status_data.get("status", "active")
            }
            
        except ValidationError:
            raise
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"更新用户状态失败: {str(e)}")
            db.rollback()
            raise DatabaseError(f"更新用户状态失败: {str(e)}")
    
    @staticmethod
    def delete_user(db: Session, user_id: str) -> Dict[str, Any]:
        """删除用户"""
        try:
            # 验证参数
            if not user_id:
                raise ValidationError("用户ID不能为空", "user_id")
            
            # 提取用户ID
            if user_id.startswith("USR-"):
                user_id = user_id[4:]
            
            # 验证用户ID格式
            try:
                user_id_int = int(user_id)
            except ValueError:
                raise ValidationError("用户ID格式不正确", "user_id")
            
            # 查询用户
            user = db.query(User).filter(User.id == user_id_int).first()
            if not user:
                raise NotFoundError("用户", user_id)
            
            # 删除用户（级联删除相关关联）
            db.delete(user)
            db.commit()
            
            return {"deleted": True}
            
        except ValidationError:
            raise
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"删除用户失败: {str(e)}")
            db.rollback()
            raise DatabaseError(f"删除用户失败: {str(e)}")
    
    @staticmethod
    def bulk_delete_users(db: Session, ids: List[str]) -> Dict[str, Any]:
        """批量删除用户"""
        try:
            if not ids:
                raise ValidationError("请提供要删除的用户ID列表", "ids")
            
            # 提取用户ID
            user_ids = []
            for user_id in ids:
                if user_id.startswith("USR-"):
                    try:
                        user_ids.append(int(user_id[4:]))
                    except ValueError:
                        raise ValidationError(f"用户ID格式不正确: {user_id}", "ids")
                else:
                    try:
                        user_ids.append(int(user_id))
                    except ValueError:
                        raise ValidationError(f"用户ID格式不正确: {user_id}", "ids")
            
            # 查询并删除用户
            deleted_count = db.query(User).filter(User.id.in_(user_ids)).delete(synchronize_session=False)
            db.commit()
            
            return {"deleted": deleted_count}
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"批量删除用户失败: {str(e)}")
            db.rollback()
            raise DatabaseError(f"批量删除用户失败: {str(e)}")
    
    @staticmethod
    def _get_user_roles_and_permissions(user: User) -> Tuple[List[str], List[str]]:
        """获取用户的角色和权限"""
        user_roles = []
        user_permissions = []
        
        try:
            for user_role in user.user_roles:
                user_roles.append(user_role.role.name)
                
                # 获取角色权限
                for role_permission in user_role.role.role_permissions:
                    user_permissions.append(role_permission.permission.name)
            
            # 去重
            user_permissions = list(set(user_permissions))
            
        except Exception as e:
            logger.warning(f"获取用户角色权限失败: {str(e)}")
            # 如果获取权限失败，设置默认值
            user_roles = ["user"]
            user_permissions = ["basic"]
            
        return user_roles, user_permissions