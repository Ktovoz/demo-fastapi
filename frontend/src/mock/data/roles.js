export const mockRoles = [
  {
    "id": 1,
    "name": "admin",
    "displayName": "系统管理员",
    "description": "拥有系统所有资源的完整访问权限",
    "status": "active",
    "permissions": [
      "dashboard:view",
      "users:view",
      "users:edit",
      "users:delete",
      "roles:view",
      "roles:edit",
      "system:manage"
    ],
    "members": 12
  },
  {
    "id": 2,
    "name": "manager",
    "displayName": "团队经理",
    "description": "管理团队成员并查看相关指标数据",
    "status": "active",
    "permissions": [
      "dashboard:view",
      "users:view",
      "users:edit",
      "logs:view"
    ],
    "members": 8
  },
  {
    "id": 3,
    "name": "support",
    "displayName": "客服人员",
    "description": "处理客户工单并监控系统事件",
    "status": "pending",
    "permissions": [
      "dashboard:view",
      "users:view",
      "logs:view"
    ],
    "members": 15
  },
  {
    "id": 4,
    "name": "user",
    "displayName": "普通用户",
    "description": "只读权限，可查看报告和仪表盘",
    "status": "inactive",
    "permissions": [
      "dashboard:view"
    ],
    "members": 21
  }
]