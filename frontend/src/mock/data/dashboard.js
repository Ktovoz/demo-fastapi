export const mockDashboard = {
  "summaryCards": [
    {
      "key": "users",
      "title": "Active Users",
      "value": 1286,
      "change": "+8.4%",
      "trend": "up"
    },
    {
      "key": "sessions",
      "title": "Sessions Today",
      "value": 342,
      "change": "-2.1%",
      "trend": "down"
    },
    {
      "key": "errors",
      "title": "System Alerts",
      "value": 3,
      "change": "stable",
      "trend": "flat"
    },
    {
      "key": "uptime",
      "title": "Uptime",
      "value": "99.98%",
      "change": "+0.01%",
      "trend": "up"
    }
  ],
  "trafficChart": {
    "labels": [
      "Mon",
      "Tue",
      "Wed",
      "Thu",
      "Fri",
      "Sat",
      "Sun"
    ],
    "series": [
      {
        "name": "API Requests",
        "data": [
          820,
          932,
          901,
          934,
          1290,
          1330,
          1320
        ]
      },
      {
        "name": "Active Users",
        "data": [
          120,
          132,
          101,
          134,
          90,
          230,
          210
        ]
      }
    ]
  },
  "recentActivities": [
    {
      "id": 1,
      "time": "2025-10-04 08:15",
      "user": "Alex",
      "action": "approved new user",
      "target": "User 1024"
    },
    {
      "id": 2,
      "time": "2025-10-04 09:30",
      "user": "System",
      "action": "synced audit logs",
      "target": "S3 bucket"
    },
    {
      "id": 3,
      "time": "2025-10-04 10:05",
      "user": "Morgan",
      "action": "updated role",
      "target": "Manager"
    },
    {
      "id": 4,
      "time": "2025-10-04 11:20",
      "user": "Jules",
      "action": "disabled account",
      "target": "User 0999"
    }
  ],
  "systemHealth": [
    {
      "label": "API Service",
      "status": "operational",
      "message": "Responding normally"
    },
    {
      "label": "Scheduler",
      "status": "degraded",
      "message": "Retrying failed jobs"
    },
    {
      "label": "Notifications",
      "status": "operational",
      "message": "Emails queued"
    },
    {
      "label": "Database",
      "status": "operational",
      "message": "Replica status healthy"
    }
  ]
}
