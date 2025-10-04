# API文档

<!-- 
文档管理规范:
- 内容：包含前后端共同需要查看的API列表，包括待实现和未实现的API，以及API规范
- 目的：为前后端开发人员提供统一的API接口参考，确保接口调用的一致性和准确性
请AI在编辑此文档时遵守上述规范
-->

## 说明
- 当前前端默认通过 `VITE_USE_MOCK=true` 调用 mock 数据，待后台实现后可直接替换为真实接口。
- 所有返回体均遵循 `{ status, data }` 的包裹规范，其中 `status` 为 HTTP 状态码，`data` 为业务数据。

## 管理驾驶舱（Mock）

### GET /admin/overview
- **用途**：获取后台驾驶舱概览，包含指标卡、趋势数据、服务健康与值班信息。
- **请求参数**：无
- **响应示例**：
```json
{
  "cards": [
    { "key": "activeUsers", "title": "活跃用户", "value": 1820, "change": "+12%" }
  ],
  "trend": [
    { "date": "10-04", "requests": 18942, "activeUsers": 802, "errorRate": 0.4 }
  ],
  "services": [
    { "key": "billing", "status": "operational", "latency": 212 }
  ],
  "shifts": [
    { "id": "SHIFT-01", "name": "晨间巡检", "readiness": 0.92 }
  ]
}
```

### GET /admin/alerts
- **用途**：拉取实时运营告警列表。
- **请求参数**：无
- **响应字段**：`id`, `severity` (`high|medium|low`), `title`, `message`, `timestamp`, `owner`, `acknowledged`。

### POST /admin/alerts/{id}/acknowledge
- **用途**：将告警标记为已处理。
- **请求参数**：路径参数 `id`
- **响应**：返回更新后的告警对象。

### GET /admin/tasks
- **用途**：分页获取跨团队任务板。
- **请求参数**：
  - `page`（默认 1）
  - `pageSize`（默认 8）
  - `status`（`todo|in_progress|review|done|all`）
  - `priority`（`high|medium|low|all`）
  - `keyword`（按标题、负责人、标签模糊匹配）
- **响应字段**：`items`（任务列表）、`total`、`page`、`pageSize`。

### PATCH /admin/tasks/{id}
- **用途**：更新任务状态或描述。
- **请求体**：支持局部字段，如 `{ "status": "done" }`
- **响应**：更新后的任务。

### POST /admin/tasks
- **用途**：创建一条新的后台任务。
- **请求体**：`title`, `assignee`, `priority`, `status`, `tags`
- **响应**：新建任务。

### GET /admin/audit-timeline
- **用途**：获取当日敏感操作审计时间线。
- **响应字段**：`actor`, `action`, `target`, `time`, `status`, `detail`。

## 系统日志（Mock）

### GET /system/logs
- **用途**：分页查询系统日志。
- **请求参数**：
  - `page`（默认 1）
  - `pageSize`（默认 10）
  - `level`（`INFO|WARN|ERROR|DEBUG|ALL`）
  - `keyword`（匹配 `message`、`module`、`context.requestId`）
  - `sorter`（示例：`{"field":"time","order":"descend"}`）
- **响应字段**：`items`（日志列表）、`total`、`page`、`pageSize`。

### GET /system/logs/summary
- **用途**：返回日志级别分布、模块热点与最近日志。
- **响应示例**：
```json
{
  "severity": { "ERROR": 8, "WARN": 12, "INFO": 20, "DEBUG": 10 },
  "topModules": [ { "module": "billing", "total": 9 } ],
  "recent": [ { "id": 46, "time": "2025-10-04 23:22:58", "level": "ERROR", "module": "notifications" } ],
  "total": 50,
  "errorRatio": 40.0
}
```

## 未来后端实现提示
- 若迁移至真实接口，请确保返回字段与上述 mock 结构保持一致，以减少前端改动。
- 需要身份校验的接口建议统一增加 `Authorization` 头部并返回 401/403 场景说明。
