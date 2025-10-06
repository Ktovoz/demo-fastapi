from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from typing import Dict, Any, List

from ..models.user import User
from ..models.role import Role
from ..models.permission import Permission
from ..models.operation_log import OperationLog
from ..utils.logger import get_logger

logger = get_logger(__name__)

class SystemInitService:
    """系统初始化服务"""

    @staticmethod
    def reset_system(db: Session) -> Dict[str, Any]:
        """
        重置系统到初始状态
        1. 清除所有数据（除了基础表结构）
        2. 重新创建初始数据
        3. 生成固定ID的基础数据
        """
        try:
            logger.info("开始系统初始化...")
            result = {
                "timestamp": datetime.utcnow().isoformat(),
                "operations": []
            }

            # 1. 清除所有表数据（按依赖关系顺序）
            tables_to_clear = [
                ("operation_logs", "操作日志表"),
                ("user_roles", "用户角色关联表"),
                ("role_permissions", "角色权限关联表"),
                ("roles", "角色表"),
                ("permissions", "权限表"),
                ("users", "用户表")
            ]

            for table_name, table_desc in tables_to_clear:
                count = db.execute(text(f"DELETE FROM {table_name}")).rowcount
                result["operations"].append(f"清空{table_desc}: {count}条记录")
                logger.info(f"清空{table_desc}: {count}条记录")

            # 2. 重新创建固定ID的基础权限
            permissions_data = [
                # 仪表盘权限
                {"id": 1, "name": "dashboard:view", "resource": "dashboard", "action": "view", "description": "查看仪表盘"},

                # 用户管理权限
                {"id": 2, "name": "users:view", "resource": "users", "action": "view", "description": "查看用户列表"},
                {"id": 3, "name": "users:create", "resource": "users", "action": "create", "description": "创建用户"},
                {"id": 4, "name": "users:edit", "resource": "users", "action": "edit", "description": "编辑用户"},
                {"id": 5, "name": "users:delete", "resource": "users", "action": "delete", "description": "删除用户"},
                {"id": 6, "name": "users:reset_password", "resource": "users", "action": "reset_password", "description": "重置用户密码"},

                # 角色管理权限
                {"id": 7, "name": "roles:view", "resource": "roles", "action": "view", "description": "查看角色列表"},
                {"id": 8, "name": "roles:create", "resource": "roles", "action": "create", "description": "创建角色"},
                {"id": 9, "name": "roles:edit", "resource": "roles", "action": "edit", "description": "编辑角色"},
                {"id": 10, "name": "roles:delete", "resource": "roles", "action": "delete", "description": "删除角色"},

                # 权限管理权限
                {"id": 11, "name": "permissions:view", "resource": "permissions", "action": "view", "description": "查看权限列表"},
                {"id": 12, "name": "permissions:edit", "resource": "permissions", "action": "edit", "description": "编辑权限"},

                # 系统管理权限
                {"id": 13, "name": "system:settings", "resource": "system", "action": "settings", "description": "系统设置管理"},
                {"id": 14, "name": "system:logs", "resource": "system", "action": "logs", "description": "查看系统日志"},
                {"id": 15, "name": "system:export", "resource": "system", "action": "export", "description": "导出系统数据"},
                {"id": 16, "name": "system:import", "resource": "system", "action": "import", "description": "导入系统数据"},
                {"id": 17, "name": "system:backup", "resource": "system", "action": "backup", "description": "系统备份"},
                {"id": 18, "name": "system:init", "resource": "system", "action": "init", "description": "系统初始化"},

                # 运营中心权限
                {"id": 19, "name": "admin:alerts", "resource": "admin", "action": "alerts", "description": "查看系统告警"},
                {"id": 20, "name": "admin:analytics", "resource": "admin", "action": "analytics", "description": "查看系统分析"},
                {"id": 21, "name": "admin:notifications", "resource": "admin", "action": "notifications", "description": "系统通知管理"},
            ]

            for perm_data in permissions_data:
                permission = Permission(**perm_data)
                db.add(permission)

            db.commit()
            result["operations"].append(f"创建权限表: {len(permissions_data)}个权限")

            # 3. 创建固定ID的角色
            roles_data = [
                {
                    "id": 1,
                    "name": "super_admin",
                    "display_name": "超级管理员",
                    "description": "系统超级管理员，拥有所有权限",
                    "permission_ids": list(range(1, 22))  # 所有权限
                },
                {
                    "id": 2,
                    "name": "admin",
                    "display_name": "管理员",
                    "description": "系统管理员，拥有大部分管理权限",
                    "permission_ids": [1, 2, 3, 4, 7, 8, 9, 13, 14, 15, 19, 20, 21]
                },
                {
                    "id": 3,
                    "name": "operator",
                    "display_name": "运营人员",
                    "description": "运营人员，可以查看和分析数据",
                    "permission_ids": [1, 2, 14, 19, 20, 21]
                },
                {
                    "id": 4,
                    "name": "user",
                    "display_name": "普通用户",
                    "description": "普通用户，只有基本查看权限",
                    "permission_ids": [1]
                }
            ]

            for role_data in roles_data:
                permission_ids = role_data.pop("permission_ids")
                role = Role(**role_data)
                db.add(role)
                db.flush()  # 确保角色被创建并获取ID

                # 添加角色权限关联
                for perm_id in permission_ids:
                    db.execute(text(
                        "INSERT INTO role_permissions (role_id, permission_id) VALUES (:role_id, :perm_id)",
                        {"role_id": role.id, "perm_id": perm_id}
                    ))

            db.commit()
            result["operations"].append(f"创建角色表: {len(roles_data)}个角色")

            # 4. 创建超级管理员用户
            from ..core.security import get_password_hash

            admin_user = User(
                id=1,  # 固定ID
                username="admin",
                email="admin@example.com",
                full_name="系统管理员",
                password_hash=get_password_hash("admin123"),
                is_active=True,
                is_superuser=True,
                avatar=None,
                last_login=None
            )
            db.add(admin_user)

            # 添加用户角色关联
            db.execute(text(
                "INSERT INTO user_roles (user_id, role_id) VALUES (1, 1)"
            ))

            db.commit()
            result["operations"].append("创建超级管理员用户: admin/admin123")

            # 5. 创建示例普通用户
            normal_user = User(
                id=2,  # 固定ID
                username="test",
                email="test@example.com",
                full_name="测试用户",
                password_hash=get_password_hash("test123"),
                is_active=True,
                is_superuser=False,
                avatar=None,
                last_login=None
            )
            db.add(normal_user)

            # 添加用户角色关联
            db.execute(text(
                "INSERT INTO user_roles (user_id, role_id) VALUES (2, 4)"
            ))

            db.commit()
            result["operations"].append("创建测试用户: test/test123")

            # 6. 创建初始操作日志（固定当前的操作日志作为基准）
            init_logs = [
                {
                    "id": 1,
                    "user_id": 1,
                    "action": "系统初始化",
                    "resource": "system",
                    "description": "系统管理员执行系统初始化",
                    "ip_address": "127.0.0.1",
                    "user_agent": "System Initialization Service"
                },
                {
                    "id": 2,
                    "user_id": 1,
                    "action": "创建超级管理员",
                    "resource": "users",
                    "description": "系统初始化创建超级管理员账号",
                    "ip_address": "127.0.0.1",
                    "user_agent": "System Initialization Service"
                },
                {
                    "id": 3,
                    "user_id": 1,
                    "action": "创建基础角色",
                    "resource": "roles",
                    "description": "系统初始化创建基础角色权限",
                    "ip_address": "127.0.0.1",
                    "user_agent": "System Initialization Service"
                },
                {
                    "id": 4,
                    "user_id": 1,
                    "action": "用户登录",
                    "resource": "auth",
                    "description": "超级管理员登录系统",
                    "ip_address": "127.0.0.1",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
                {
                    "id": 5,
                    "user_id": 1,
                    "action": "查看系统设置",
                    "resource": "system",
                    "description": "管理员查看系统配置页面",
                    "ip_address": "127.0.0.1",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
                {
                    "id": 6,
                    "user_id": 1,
                    "action": "查看操作日志",
                    "resource": "system",
                    "description": "管理员查看系统操作日志",
                    "ip_address": "127.0.0.1",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
                {
                    "id": 7,
                    "user_id": 2,
                    "action": "用户登录",
                    "resource": "auth",
                    "description": "测试用户登录系统",
                    "ip_address": "127.0.0.1",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
                {
                    "id": 8,
                    "user_id": 2,
                    "action": "查看仪表盘",
                    "resource": "dashboard",
                    "description": "用户查看系统仪表盘",
                    "ip_address": "127.0.0.1",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
                {
                    "id": 9,
                    "user_id": 1,
                    "action": "修改系统设置",
                    "resource": "system",
                    "description": "管理员修改系统配置参数",
                    "ip_address": "127.0.0.1",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
            ]

            for log_data in init_logs:
                log = OperationLog(**log_data)
                db.add(log)

            db.commit()
            result["operations"].append(f"创建初始操作日志: {len(init_logs)}条")

            # 记录完成
            result["success"] = True
            result["message"] = "系统初始化完成"
            result["created_at"] = datetime.utcnow().isoformat()
            result["summary"] = {
                "users": 2,
                "roles": 4,
                "permissions": 21,
                "logs": 9  # 固定9条初始操作日志
            }

            logger.info(f"系统初始化完成: {result['summary']}")
            return result

        except Exception as e:
            logger.error(f"系统初始化失败: {str(e)}")
            db.rollback()
            raise Exception(f"系统初始化失败: {str(e)}")

    @staticmethod
    def get_system_status(db: Session) -> Dict[str, Any]:
        """获取系统当前状态"""
        try:
            status = {
                "timestamp": datetime.utcnow().isoformat(),
                "database_status": "connected",
                "data_counts": {},
                "last_init": None,
                "needs_init": False
            }

            # 统计各表数据量
            tables = ["users", "roles", "permissions", "operation_logs"]
            for table in tables:
                count = db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                status["data_counts"][table] = count

            # 检查是否需要初始化
            if status["data_counts"]["users"] == 0:
                status["needs_init"] = True
                status["message"] = "系统未初始化，需要执行初始化"
            else:
                status["message"] = "系统正常运行"

            # 查找最近的初始化日志
            init_log = db.query(OperationLog).filter(
                OperationLog.action == "系统初始化"
            ).order_by(OperationLog.created_at.desc()).first()

            if init_log:
                status["last_init"] = init_log.created_at.isoformat()

            return status

        except Exception as e:
            logger.error(f"获取系统状态失败: {str(e)}")
            raise Exception(f"获取系统状态失败: {str(e)}")