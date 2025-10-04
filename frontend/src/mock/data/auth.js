export const mockAccounts = [
  {
    "email": "admin@example.com",
    "password": "admin123",
    "id": 1,
    "name": "Admin User",
    "role": "admin",
    "permissions": [
      "*"
    ],
    "lastLogin": "2025-10-04T09:00:00Z"
  },
  {
    "email": "manager@example.com",
    "password": "manager123",
    "id": 2,
    "name": "Team Manager",
    "role": "manager",
    "permissions": [
      "dashboard:view",
      "users:view",
      "users:edit"
    ],
    "lastLogin": "2025-10-03T18:12:00Z"
  },
  {
    "email": "support@example.com",
    "password": "support123",
    "id": 3,
    "name": "Support Agent",
    "role": "support",
    "permissions": [
      "dashboard:view",
      "logs:view"
    ],
    "lastLogin": "2025-09-29T11:45:00Z"
  }
]
