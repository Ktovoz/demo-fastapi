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
        
        # 创建默认权限 - 完整版，匹配前端权限需求
        permissions = [
            # 仪表盘权限
            Permission(
                name="dashboard:view",
                resource="dashboard",
                action="view",
                description="查看仪表盘权限"
            ),
            # 用户管理权限
            Permission(
                name="users:view",
                resource="users",
                action="view",
                description="查看用户列表权限"
            ),
            Permission(
                name="users:edit",
                resource="users",
                action="edit",
                description="编辑用户权限"
            ),
            Permission(
                name="users:create",
                resource="users",
                action="create",
                description="创建用户权限"
            ),
            Permission(
                name="users:delete",
                resource="users",
                action="delete",
                description="删除用户权限"
            ),
            # 角色管理权限
            Permission(
                name="roles:view",
                resource="roles",
                action="view",
                description="查看角色列表权限"
            ),
            Permission(
                name="roles:edit",
                resource="roles",
                action="edit",
                description="编辑角色权限"
            ),
            Permission(
                name="roles:create",
                resource="roles",
                action="create",
                description="创建角色权限"
            ),
            Permission(
                name="roles:delete",
                resource="roles",
                action="delete",
                description="删除角色权限"
            ),
            # 系统管理权限
            Permission(
                name="system:manage",
                resource="system",
                action="manage",
                description="系统管理权限"
            ),
            Permission(
                name="logs:view",
                resource="logs",
                action="view",
                description="查看日志权限"
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
        db.refresh(admin_user)

        # 为管理员角色分配所有权限
        logger.info("正在为管理员角色分配权限...")
        for permission in permissions:
            from ..models.role_permission import RolePermission
            role_permission = RolePermission(
                role_id=admin_role.id,
                permission_id=permission.id
            )
            db.add(role_permission)

        # 为普通用户角色分配基本权限
        logger.info("正在为普通用户角色分配基本权限...")
        basic_permission_names = [
            "dashboard:view",
            "users:view",
            "roles:view"
        ]

        basic_permissions = []
        for permission in permissions:
            if permission.name in basic_permission_names:
                basic_permissions.append(permission)
                from ..models.role_permission import RolePermission
                role_permission = RolePermission(
                    role_id=user_role.id,
                    permission_id=permission.id
                )
                db.add(role_permission)

        # 为管理员用户分配管理员角色
        logger.info("正在为管理员用户分配角色...")
        from ..models.user_role import UserRole
        user_role_assignment = UserRole(
            user_id=admin_user.id,
            role_id=admin_role.id
        )
        db.add(user_role_assignment)

        db.commit()
        logger.info(f"管理员用户已分配角色: {admin_role.name}")
        logger.info(f"管理员角色已分配权限数量: {len(permissions)}")
        logger.info(f"普通用户角色已分配权限数量: {len(basic_permissions)}")

        logger.info("默认数据初始化完成")
        logger.info(f"默认管理员账号: {settings.DEFAULT_ADMIN_USERNAME}")
        logger.info(f"默认管理员密码: {settings.DEFAULT_ADMIN_PASSWORD}")
        logger.info(f"管理员用户已分配角色: {admin_role.name}")
        logger.info(f"管理员角色已分配权限数量: {len(permissions)}")
        
    except Exception as e:
        logger.error(f"初始化默认数据失败: {e}")
        raise