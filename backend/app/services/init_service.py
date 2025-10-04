from sqlalchemy.orm import Session
from ..core.config import settings
from ..core.security import get_password_hash
from ..models.user import User
from ..models.role import Role
from ..models.permission import Permission
from ..utils.logger import get_logger

logger = get_logger(__name__)

def init_default_data(db: Session):
    """初始化默认数据"""
    try:
        # 检查是否已经初始化过
        admin_user = db.query(User).filter(User.username == settings.DEFAULT_ADMIN_USERNAME).first()
        if admin_user:
            logger.info("默认数据已经存在，跳过初始化")
            return
        
        logger.info("开始初始化默认数据")
        
        # 创建默认权限 - 简化版，只创建基本权限
        permissions = [
            Permission(
                name="user:read",
                resource="user",
                action="read",
                description="查看用户权限"
            ),
            Permission(
                name="user:create",
                resource="user",
                action="create",
                description="创建用户权限"
            ),
            Permission(
                name="user:update",
                resource="user",
                action="update",
                description="更新用户权限"
            ),
            Permission(
                name="user:delete",
                resource="user",
                action="delete",
                description="删除用户权限"
            ),
        ]
        
        for permission in permissions:
            db.add(permission)
        
        db.commit()
        
        # 创建默认角色
        admin_role = Role(
            name="admin",
            description="系统管理员，拥有所有权限"
        )
        
        user_role = Role(
            name="user",
            description="普通用户"
        )
        
        db.add(admin_role)
        db.add(user_role)
        db.commit()
        
        # 创建默认管理员用户
        admin_user = User(
            username=settings.DEFAULT_ADMIN_USERNAME,
            email=settings.DEFAULT_ADMIN_EMAIL,
            password_hash=get_password_hash(settings.DEFAULT_ADMIN_PASSWORD),
            full_name="系统管理员",
            is_superuser=True,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        
        logger.info("默认数据初始化完成")
        logger.info(f"默认管理员账号: {settings.DEFAULT_ADMIN_USERNAME}")
        logger.info(f"默认管理员密码: {settings.DEFAULT_ADMIN_PASSWORD}")
        
    except Exception as e:
        logger.error(f"初始化默认数据失败: {e}")
        raise