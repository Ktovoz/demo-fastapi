from sqlalchemy.orm import Session
from ..models.user import User
from ..models.role import Role
from ..models.permission import Permission
from ..models.user_role import UserRole
from ..models.role_permission import RolePermission
from ..core.security import get_password_hash, verify_password
from ..utils.logger import get_logger
from ..utils.exceptions import ValidationError, NotFoundError, DatabaseError
from typing import List, Dict, Any, Tuple
import datetime

logger = get_logger(__name__)

class UserService:
    """用户相关服务"""
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """根据用户名获取用户"""
        # 验证参数
        if not username:
            raise ValidationError("用户名不能为空", "username")
        
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """根据邮箱获取用户"""
        # 验证参数
        if not email:
            raise ValidationError("邮箱不能为空", "email")
        
        # 验证邮箱格式
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_roles_and_permissions(db: Session, user: User) -> Tuple[List[str], List[str]]:
        """获取用户的角色和权限"""
        user_roles = []
        user_permissions = []
        
        try:
            # 获取用户角色
            for user_role in user.user_roles:
                role = user_role.role
                user_roles.append(role.name)
                
                # 获取角色权限
                for role_permission in role.role_permissions:
                    permission = role_permission.permission
                    user_permissions.append(permission.name)
            
            # 去重
            user_permissions = list(set(user_permissions))
            
        except Exception as e:
            logger.error(f"获取用户角色权限失败: {str(e)}")
            # 如果获取权限失败，设置默认值
            user_roles = ["user"]
            user_permissions = ["basic"]
            
        return user_roles, user_permissions
    
    @staticmethod
    def update_last_login(db: Session, user: User):
        """更新用户最后登录时间"""
        try:
            user.last_login = datetime.datetime.utcnow()
            db.commit()
        except Exception as e:
            logger.error(f"更新用户最后登录时间失败: {str(e)}")
            db.rollback()
            raise DatabaseError(f"更新用户最后登录时间失败: {str(e)}")
    
    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str, full_name: str = None) -> User:
        """创建新用户"""
        try:
            # 验证参数
            if not username:
                raise ValidationError("用户名不能为空", "username")
            
            if not email:
                raise ValidationError("邮箱不能为空", "email")
            
            if not password:
                raise ValidationError("密码不能为空", "password")
            
            # 验证邮箱格式
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                raise ValidationError("邮箱格式不正确", "email")
            
            hashed_password = get_password_hash(password)
            new_user = User(
                username=username,
                email=email,
                password_hash=hashed_password,
                full_name=full_name
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            return new_user
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"创建用户失败: {str(e)}")
            db.rollback()
            raise DatabaseError(f"创建用户失败: {str(e)}")
    
    @staticmethod
    def assign_default_role(db: Session, user: User):
        """为用户分配默认角色"""
        try:
            # 验证参数
            if not user:
                raise ValidationError("用户不能为空", "user")
            
            # 查找普通用户角色
            user_role = db.query(Role).filter(Role.name == "user").first()
            
            if not user_role:
                logger.warning("未找到普通用户角色，创建默认角色...")
                # 如果不存在，创建默认用户角色
                user_role = Role(
                    name="user",
                    description="普通用户，拥有基本查看权限"
                )
                db.add(user_role)
                db.commit()
                db.refresh(user_role)
                
                # 为普通用户角色分配基本权限
                basic_permissions = db.query(Permission).filter(
                    Permission.name.in_([
                        "dashboard:view",
                        "users:view",
                        "roles:view"
                    ])
                ).all()
                
                for permission in basic_permissions:
                    role_permission = RolePermission(
                        role_id=user_role.id,
                        permission_id=permission.id
                    )
                    db.add(role_permission)
                
                db.commit()
                            
            # 将用户分配到普通用户角色
            user_role_assignment = UserRole(
                user_id=user.id,
                role_id=user_role.id
            )
            db.add(user_role_assignment)
            db.commit()
            
            logger.info(f"用户 {user.username} 已分配默认角色: {user_role.name}")
            
        except Exception as e:
            logger.error(f"为用户分配默认角色失败: {str(e)}")
            db.rollback()
            raise DatabaseError(f"为用户分配默认角色失败: {str(e)}")

class AuthService:
    """认证相关服务"""
    
    @staticmethod
    def verify_user_credentials(db: Session, username: str, password: str) -> User:
        """验证用户凭据"""
        # 验证参数
        if not username:
            raise ValidationError("用户名不能为空", "username")
        
        if not password:
            raise ValidationError("密码不能为空", "password")
        
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None
            
        if not verify_password(password, user.password_hash):
            return None
            
        return user
    
    @staticmethod
    def verify_user_credentials_by_email(db: Session, email: str, password: str) -> User:
        """通过邮箱验证用户凭据"""
        # 验证参数
        if not email:
            raise ValidationError("邮箱不能为空", "email")
        
        if not password:
            raise ValidationError("密码不能为空", "password")
        
        user = UserService.get_user_by_email(db, email)
        if not user:
            return None
            
        if not verify_password(password, user.password_hash):
            return None
            
        return user