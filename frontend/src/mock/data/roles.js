export const mockRoles = [
  {
    "id": 1,
    "name": "admin",
    "displayName": "Administrator",
    "description": "Full access to all resources",
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
    "displayName": "Team Manager",
    "description": "Manage team members and review metrics",
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
    "displayName": "Support Agent",
    "description": "Resolve customer tickets and monitor incidents",
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
    "name": "viewer",
    "displayName": "Read Only",
    "description": "Read-only access to reports and dashboards",
    "status": "inactive",
    "permissions": [
      "dashboard:view"
    ],
    "members": 21
  }
]
