# API文档

## 说明
- 本文基于 2025-10-04 的前端实现整理，供后端开发对接参考。
- 前端默认 API Base URL 为 `http://localhost:8000`，可通过运行时的 `window.APP_CONFIG.API_BASE_URL` 覆盖。
- 除登录、注册、找回密码外，其余请求均需携带 `Authorization: Bearer <token>` 请求头。

## 全局约定
- 所有接口返回 `application/json`，Axios 直接消费响应体。
- 列表型接口需返回 `{ "items": [], "total": 0, "page": 1, "pageSize": 10 }` 结构；`items` 内部字段见各小节。
- 排序统一使用 `sorter` 对象，格式：`{"field": "time", "order": "descend"}`，`order` 取值 `ascend|descend`。
- 前端会把未筛选的枚举传为 `"all"`，多选类筛选传空数组，后端需要兼容视为"忽略过滤"。
- 失败响应至少返回 `message` 或 `detail` 字段，便于前端展示错误；401 状态会触发前端登出流程。

## 连通性/健康检查

### GET /health
- **用途**：用于部署后验证后端可用性与前后端连通性，CI/CD 和监控探针均可调用。
- **请求参数**：无。
- **响应体**：
```json
{
  "status": "ok",
  "timestamp": "2025-10-04T16:32:00Z",
  "version": "1.0.0"
}
```
- **说明**：
  - `status` 取值 `ok|degraded`；非 `ok` 时应返回 `detail` 描述。
  - `timestamp` 为 ISO 8601 时间，便于排查缓存与验证链路。
  - `version` 可选，返回后端当前构建号以供前端排错。

---

## 认证模块

### POST /auth/login
- **用途**：邮箱 + 密码登录，返回访问令牌及当前用户信息。
- **请求体**：
```json
{
  "email": "admin@example.com",
  "password": "secret",
  "remember": true
}
```
- **响应体**：
```json
{
  "token": "jwt-token",
  "expiresIn": 120,
  "user": {
    "id": "USR-001",
    "name": "Demo Admin",
    "email": "admin@example.com",
    "role": "admin",
    "permissions": ["*"],
    "avatar": "https://.../avatar.png",
    "lastLogin": "2025-10-04T03:20:00Z"
  }
}
```
- **说明**：`remember` 为布尔值，可用于延长会话；若返回 `expiresIn`（分钟），前端会计算绝对过期时间。

### POST /auth/login-json
- **用途**：JSON格式登录，支持记住我功能。
- **请求体**：
```json
{
  "email": "admin@example.com",
  "password": "secret",
  "remember": true
}
```
- **响应体**：同 `/auth/login`

### POST /auth/register
- **用途**：创建新账号。
- **请求体**：`{ "name": string, "email": string, "password": string }`
- **响应体**：返回成功提示或 `{ "id": "USR-002" }`（前端只检查响应为 2xx）。

### POST /auth/forgot-password
- **用途**：发送密码重置邮件。
- **请求体**：`{ "email": string }`
- **响应体**：返回 `{ "status": "sent" }` 或空体均可。

---

## 仪表盘（/dashboard）

### GET /dashboard/metrics
- **用途**：仪表盘首页核心数据。
- **响应体关键字段**：
  - `summaryCards`: 数组。每项 `{ key: "users", title, value, unit?, change, changeType, trend, trendLabel?, description?, icon }`
    - `icon` 取值：`TeamOutlined|RiseOutlined|DashboardOutlined|AlertOutlined`。
    - `trend` 取值：`up|down|flat`。
  - `trafficChart`: `{ labels: ["10-01"], series: [{ name: "API Requests", data: [1820] }, { name: "Active Users", data: [640] }] }`
  - `systemHealth`: 数组，每项 `{ label, status, message }`，`status` 取 `operational|degraded|down`。
  - `recentActivities`: 数组，每项 `{ id, time, user, action, target }`。
- **前端依赖**：字段缺失会导致图表空白，请保证数组至少返回空数组。

### GET /dashboard/overview
- **用途**：备用概览接口（当前页面未直接使用，可与 `metrics` 同步字段，后续用于渐进式加载）。

---

## 用户管理（/users）

### GET /users
- **用途**：用户列表分页查询。
- **查询参数**：
  - `page`（默认 1）、`pageSize`（默认 10）。
  - `keyword`: 按姓名 / 邮箱模糊搜索。
  - `status`: `active|inactive|pending|all`。
  - `role`: 角色标识或 `all`。
  - `tags`: 字符串数组。
  - `department`: 字符串数组。
  - `sorter`: JSON 字符串或对象，字段如 `{ "field": "lastLogin", "order": "descend" }`。
- **响应体**：
```json
{
  "items": [
    {
      "id": "USR-001",
      "name": "Demo Admin",
      "email": "admin@example.com",
      "role": "admin",
      "roleName": "Administrator",
      "department": "Operations",
      "status": "active",
      "lastLogin": "2025-10-04T00:12:00Z",
      "avatar": "https://...",
      "tags": ["North America"],
      "permissions": ["users:view"]
    }
  ],
  "total": 128,
  "page": 1,
  "pageSize": 10
}
```

### GET /users/{id}
- **用途**：获取单个用户详情。
- **响应字段**：`id, name, email, role, roleName, status, department, phone, tags[], permissions[], avatar, createdAt, lastLogin`。

### POST /users
- **用途**：创建用户。
- **请求体示例**：
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "role": "manager",
  "status": "active",
  "department": "Engineering",
  "phone": "+1-555-0100",
  "tags": ["LATAM"],
  "permissions": ["users:view", "users:edit"]
}
```
- **响应**：返回完整用户对象（字段同 GET /users/{id}）。

### PUT /users/{id}
- **用途**：更新用户基础信息及权限；请求体验证与创建相同。
- **响应**：返回更新后的用户对象。

### PATCH /users/{id}/status
- **用途**：切换启用 / 禁用状态。
- **响应**：返回最新用户对象（至少包含 `id`、`status`）。

### DELETE /users/{id}
- **用途**：删除单个用户。
- **响应**：`{ "deleted": true }` 或 204 空体。

### POST /users/bulk-delete
- **用途**：批量删除。
- **请求体**：`{ "ids": ["USR-002", "USR-003"] }`
- **响应**：`{ "deleted": 2 }`。

---

## 角色管理（/roles）

### GET /roles
- **用途**：获取全部角色列表。
- **响应项字段**：`id, displayName, description, members (数字), permissions[], status`。

### GET /roles/{id}
- **用途**：角色详情。
- **响应字段**：`displayName, description, permissions[], status`（用于编辑表单）。

### PUT /roles/{id}
- **用途**：更新角色名称、描述、权限与状态。
- **请求体**：与详情字段一致。
- **响应**：返回更新后的角色对象。

---

## 后台运营管理（/admin）

### GET /admin/overview
- **用途**：获取运营总览数据。
- **响应体关键字段**：
  - `cards`: 数组。每项 `{ key: "users", title, value, unit?, change, changeType, description, icon, trendLabel }`
    - `icon` 取值：`TeamOutlined|UserAddOutlined|RiseOutlined|DashboardOutlined`。
  - `trend`: `{ date: "10-01", requests: 18200, activeUsers: 1200, errorRate: 0.5 }`
  - `services`: 数组，每项 `{ key, name, owner, status, uptime, latency, change }`，`status` 取 `operational|degraded|down`。
  - `shifts`: 数组，每项 `{ id, name, window, lead, readiness }`。

### GET /admin/alerts
- **用途**：获取告警列表。
- **响应体**：
```json
[
  {
    "id": "alert-1",
    "severity": "high",
    "title": "API服务响应时间异常",
    "message": "API服务平均响应时间超过500ms阈值",
    "timestamp": "2025-10-04T10:30:00Z",
    "owner": "技术团队",
    "acknowledged": false
  }
]
```

### POST /admin/alerts/{alert_id}/acknowledge
- **用途**：确认告警。
- **响应体**：返回确认后的告警对象。

### GET /admin/tasks
- **用途**：获取任务列表。
- **查询参数**：
  - `page`（默认 1）、`pageSize`（默认 6）。
  - `status`: `todo|in_progress|review|done|all`。
  - `priority`: `low|medium|high|all`。
  - `keyword`: 关键词搜索。
  - `tags`: 标签筛选。
  - `sorter`: JSON 字符串或对象，字段如 `{ "field": "due", "order": "ascend" }`。
- **响应体**：
```json
{
  "items": [
    {
      "id": "task-1",
      "title": "优化API响应时间",
      "assignee": "张三",
      "due": "2025-10-06",
      "priority": "high",
      "status": "in_progress",
      "tags": ["性能优化", "后端"],
      "avatarColor": "#f50"
    }
  ],
  "total": 8,
  "page": 1,
  "pageSize": 6
}
```

### POST /admin/tasks
- **用途**：创建任务。
- **请求体**：`{ "title": string, "assignee": string, "priority": "low|medium|high", "status": "todo|in_progress|review|done", "tags": string[] }`
- **响应体**：返回创建后的任务对象。

### PATCH /admin/tasks/{task_id}
- **用途**：更新任务。
- **请求体**：可包含 `title`, `assignee`, `due`, `priority`, `status`, `tags` 等字段。
- **响应体**：返回更新后的任务对象。

### GET /admin/audit-timeline
- **用途**：获取审计时间线。
- **响应体**：
```json
[
  {
    "id": "audit-1",
    "time": "2025-10-04 10:30:00",
    "actor": "张三",
    "action": "登录系统",
    "target": "/auth/login",
    "detail": "用户登录成功",
    "status": "success"
  }
]
```

---

## 系统日志与配置（/system）

### GET /system/logs
- **用途**：分页查询系统日志。
- **查询参数**：
  - `page`（默认 1）、`pageSize`（默认 10）。
  - `keyword`：匹配 `message`、`module`、`context.requestId`。
  - `level`：`INFO|WARN|ERROR|DEBUG|ALL`。
  - `sorter`：默认 `{ "field": "time", "order": "descend" }`。
- **响应体**：
```json
{
  "items": [
    {
      "id": "LOG-001",
      "time": "2025-10-04 23:12:11",
      "level": "ERROR",
      "module": "billing",
      "message": "Payment webhook failed",
      "context": {
        "requestId": "req-1a2b3c",
        "ip": "203.0.113.10"
      }
    }
  ],
  "total": 240,
  "page": 1,
  "pageSize": 10
}
```

### GET /system/logs/summary
- **用途**：日志概览数据。
- **响应字段**：
```json
{
  "severity": { "ERROR": 8, "WARN": 12, "INFO": 20, "DEBUG": 10 },
  "recent": [{ "id": "LOG-050", "time": "2025-10-04 22:58:00", "level": "ERROR", "module": "notifications", "message": "Provider timeout" }],
  "topModules": [{ "module": "billing", "total": 9 }],
  "total": 50,
  "errorRatio": 40.0
}
```

### GET /system/settings
- **用途**：读取系统配置。
- **响应体**：
```json
{
  "appName": "Demo FastAPI Platform",
  "language": "en",
  "timezone": "UTC",
  "theme": "light",
  "notifications": { "email": true, "sms": false, "inApp": true },
  "security": { "mfa": true, "sessionTimeout": 30, "passwordPolicy": "长度≥12，含数字和特殊字符" }
}
```

### PUT /system/settings
- **用途**：更新系统配置。
- **请求体**：同 `GET /system/settings` 返回体结构。
- **响应**：返回保存后的最新配置。

---

## 通用错误示例
```json
{
  "message": "Email already exists"
}
```
或
```json
{
  "detail": "Invalid credentials"
}
```

---

## 待确认 / 后续工作
- `/dashboard/overview` 当前未在页面使用，可与 `/dashboard/metrics` 返回体保持一致或作为预聚合接口。
- 前端仍保留 Mock 切换逻辑，后端上线后请确保 `.env` 中关闭 `VITE_USE_MOCK` 并按上述字段返回，以避免渲染异常。

---

## 后端开发待办清单
- **认证模块**
  - [x] POST /auth/login —— 实现账号密码登录，返回 token、expiresIn、user。
  - [x] POST /auth/login-json —— 支持JSON格式登录，支持记住我功能。
  - [x] POST /auth/register —— 支持创建账号，校验邮箱重复。
  - [x] POST /auth/forgot-password —— 发送重置邮件并返回发送状态。
- **仪表盘**
  - [x] GET /dashboard/metrics —— 聚合 summaryCards、trafficChart、systemHealth、recentActivities。
  - [x] GET /dashboard/overview —— 按 metrics 同步结构，预留渐进加载。
- **用户管理**
  - [x] GET /users —— 支持多条件分页筛选及 sorter。
  - [x] GET /users/{id} —— 返回完整用户详情字段。
  - [x] POST /users —— 创建用户，校验必填字段。
  - [x] PUT /users/{id} —— 更新基础信息、权限、状态。
  - [x] PATCH /users/{id}/status —— 切换启用/禁用并返回最新状态。
  - [x] DELETE /users/{id} —— 单个删除返回删除结果。
  - [x] POST /users/bulk-delete —— 接收 ids 数组执行批量删除。
- **角色管理**
  - [x] GET /roles —— 返回全部角色列表。
  - [x] GET /roles/{id} —— 提供编辑所需详情。
  - [x] PUT /roles/{id} —— 更新 displayName、description、permissions、status。
- **后台运营管理**
  - [x] GET /admin/overview —— 返回运营总览数据。
  - [x] GET /admin/alerts —— 返回告警列表。
  - [x] POST /admin/alerts/{alert_id}/acknowledge —— 确认告警。
  - [x] GET /admin/tasks —— 返回任务列表。
  - [x] POST /admin/tasks —— 创建任务。
  - [x] PATCH /admin/tasks/{task_id} —— 更新任务。
  - [x] GET /admin/audit-timeline —— 返回审计时间线。
- **系统管理**
  - [x] GET /system/logs —— 分页返回日志列表及 context。
  - [x] GET /system/logs/summary —— 汇总 severity、topModules、recent、errorRatio。
  - [x] GET /system/settings —— 读取 config，含 notifications/security。
  - [x] PUT /system/settings —— 保存配置并返回最新值。
- **通用/错误处理**
  - [x] 统一错误响应 —— 返回 message/detail 字段，覆盖 4xx/5xx。
  - [x] 权限校验 —— 401/403 正确落地，触发前端登出或拒绝访问。
  - [x] GET /health —— 返回 status/timestamp/version，供探针和前端检测使用。