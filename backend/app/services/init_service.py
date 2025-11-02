from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json
from ..core.config import settings
from ..core.security import get_password_hash
from ..models.user import User
from ..models.role import Role
from ..models.permission import Permission
from ..models.operation_log import OperationLog
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
        
        # 使用 merge 替代 add，避免重复插入已存在的权限
        for permission in permissions:
            existing = db.query(Permission).filter(Permission.name == permission.name).first()
            if not existing:
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
            existing = db.query(RolePermission).filter(
                RolePermission.role_id == admin_role.id,
                RolePermission.permission_id == permission.id
            ).first()
            if not existing:
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
                existing = db.query(RolePermission).filter(
                    RolePermission.role_id == user_role.id,
                    RolePermission.permission_id == permission.id
                ).first()
                if not existing:
                    role_permission = RolePermission(
                        role_id=user_role.id,
                        permission_id=permission.id
                    )
                    db.add(role_permission)

        # 为管理员用户分配管理员角色
        logger.info("正在为管理员用户分配角色...")
        from ..models.user_role import UserRole
        existing = db.query(UserRole).filter(
            UserRole.user_id == admin_user.id,
            UserRole.role_id == admin_role.id
        ).first()
        if not existing:
            user_role_assignment = UserRole(
                user_id=admin_user.id,
                role_id=admin_role.id
            )
            db.add(user_role_assignment)

        # 创建示例操作日志
        logger.info("正在创建示例操作日志...")
        sample_logs = [
            {
                "user_id": admin_user.id,
                "action": "ERROR billing",
                "resource": "Payment webhook failed",
                "description": "支付网关回调失败，订单ID: ORD-12345",
                "ip_address": "203.0.113.10",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "request_data": {"order_id": "ORD-12345", "amount": 99.99},
                "response_data": {"status": "failed", "error": "timeout"},
                "created_at": datetime.utcnow() - timedelta(minutes=30)
            },
            {
                "user_id": admin_user.id,
                "action": "WARN auth",
                "resource": "Multiple failed login attempts",
                "description": "用户user@example.com多次登录失败",
                "ip_address": "192.0.2.45",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "request_data": {"username": "user@example.com"},
                "response_data": {"attempts": 5, "locked": True},
                "created_at": datetime.utcnow() - timedelta(hours=1)
            },
            {
                "user_id": admin_user.id,
                "action": "INFO user",
                "resource": "User profile updated",
                "description": "用户更新个人资料",
                "ip_address": "198.51.100.22",
                "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                "request_data": {"user_id": 2, "fields": ["email", "phone"]},
                "response_data": {"success": True},
                "created_at": datetime.utcnow() - timedelta(hours=2)
            },
            {
                "user_id": admin_user.id,
                "action": "ERROR notifications",
                "resource": "Provider timeout",
                "description": "通知服务提供商响应超时",
                "ip_address": "203.0.113.55",
                "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15",
                "request_data": {"provider": "sms-gateway", "recipients": 10},
                "response_data": {"status": "timeout", "sent": 3},
                "created_at": datetime.utcnow() - timedelta(hours=3)
            },
            {
                "user_id": admin_user.id,
                "action": "DEBUG system",
                "resource": "Cache cleanup completed",
                "description": "系统缓存清理完成",
                "ip_address": "192.0.2.99",
                "user_agent": "System/1.0",
                "request_data": {"operation": "cache_clear"},
                "response_data": {"cleared": 1250, "duration": "2.3s"},
                "created_at": datetime.utcnow() - timedelta(hours=4)
            },
            {
                "user_id": admin_user.id,
                "action": "INFO api",
                "resource": "API rate limit exceeded",
                "description": "API调用频率超限",
                "ip_address": "198.51.100.33",
                "user_agent": "curl/7.68.0",
                "request_data": {"endpoint": "/api/users", "client": "mobile-app"},
                "response_data": {"limit": 1000, "current": 1001},
                "created_at": datetime.utcnow() - timedelta(hours=5)
            },
            {
                "user_id": admin_user.id,
                "action": "WARN database",
                "resource": "Slow query detected",
                "description": "检测到慢查询",
                "ip_address": "203.0.113.77",
                "user_agent": "PostgreSQL/13.3",
                "request_data": {"query": "SELECT * FROM users WHERE...", "duration": "5.2s"},
                "response_data": {"optimized": False, "suggestion": "add_index"},
                "created_at": datetime.utcnow() - timedelta(hours=6)
            },
            {
                "user_id": admin_user.id,
                "action": "ERROR security",
                "resource": "Suspicious activity detected",
                "description": "检测到可疑活动",
                "ip_address": "192.0.2.88",
                "user_agent": "Unknown/0.0",
                "request_data": {"pattern": "brute_force", "target": "admin"},
                "response_data": {"blocked": True, "risk_level": "high"},
                "created_at": datetime.utcnow() - timedelta(hours=7)
            },
            {
                "user_id": admin_user.id,
                "action": "INFO users",
                "resource": "User created",
                "description": "创建新用户",
                "ip_address": "198.51.100.44",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "request_data": {"username": "newuser", "role": "user"},
                "response_data": {"user_id": 3, "success": True},
                "created_at": datetime.utcnow() - timedelta(hours=8)
            },
            {
                "user_id": admin_user.id,
                "action": "INFO roles",
                "resource": "Role permissions updated",
                "description": "更新角色权限",
                "ip_address": "203.0.113.22",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "request_data": {"role_id": 2, "permissions": ["users:view", "dashboard:view"]},
                "response_data": {"updated": True, "permissions_count": 2},
                "created_at": datetime.utcnow() - timedelta(hours=9)
            }
        ]
        
        for log_data in sample_logs:
            log = OperationLog(**log_data)
            db.add(log)
        
        db.commit()
        logger.info(f"已创建 {len(sample_logs)} 条示例操作日志")

        db.commit()
        logger.info(f"管理员用户已分配角色: {admin_role.name}")
        logger.info(f"管理员角色已分配权限数量: {len(permissions)}")
        logger.info(f"普通用户角色已分配权限数量: {len(basic_permissions)}")

        logger.info("默认数据初始化完成")
        logger.info(f"默认管理员账号: {settings.DEFAULT_ADMIN_USERNAME}")
        logger.info(f"默认管理员密码: {settings.DEFAULT_ADMIN_PASSWORD}")
        logger.info(f"管理员用户已分配角色: {admin_role.name}")
        logger.info(f"管理员角色已分配权限数量: {len(permissions)}")
        logger.info(f"已创建示例操作日志数量: {len(sample_logs)}")
        
    except Exception as e:
        logger.error(f"初始化默认数据失败: {e}")
        raise