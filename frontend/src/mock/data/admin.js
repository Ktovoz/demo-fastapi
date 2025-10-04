export const adminOverviewCards = [
  {
    key: 'activeUsers',
    title: '活跃用户',
    value: 1820,
    unit: '',
    change: '+12%',
    changeType: 'up',
    trendLabel: '较上周',
    icon: 'TeamOutlined',
    description: '近 24 小时保持 97% 的登录转化率'
  },
  {
    key: 'conversionRate',
    title: '转化率',
    value: 38.6,
    unit: '%',
    change: '+3.2%',
    changeType: 'up',
    trendLabel: '完成 Onboarding',
    icon: 'RiseOutlined',
    description: '运营活动带来额外 68 个增量用户'
  },
  {
    key: 'avgLatency',
    title: '平均响应',
    value: 182,
    unit: 'ms',
    change: '-21ms',
    changeType: 'down',
    trendLabel: '核心接口',
    icon: 'DashboardOutlined',
    description: '慢查询优化已稳定上线 18 小时'
  },
  {
    key: 'escalations',
    title: '升级工单',
    value: 6,
    unit: '条',
    change: '-2',
    changeType: 'down',
    trendLabel: '今日新增',
    icon: 'AlertOutlined',
    description: '优先处理超 12 小时的待续工单'
  }
]

export const adminTrafficTrend = [
  { date: '09-28', requests: 12840, activeUsers: 640, errorRate: 0.6 },
  { date: '09-29', requests: 14210, activeUsers: 682, errorRate: 0.4 },
  { date: '09-30', requests: 15234, activeUsers: 705, errorRate: 0.5 },
  { date: '10-01', requests: 13652, activeUsers: 688, errorRate: 0.7 },
  { date: '10-02', requests: 16108, activeUsers: 731, errorRate: 0.5 },
  { date: '10-03', requests: 17496, activeUsers: 768, errorRate: 0.3 },
  { date: '10-04', requests: 18942, activeUsers: 802, errorRate: 0.4 }
]

export const adminServiceHealth = [
  {
    key: 'billing',
    name: 'Billing Service',
    status: 'operational',
    latency: 212,
    change: -18,
    uptime: '99.96%',
    owner: 'Payments'
  },
  {
    key: 'scheduler',
    name: 'Task Scheduler',
    status: 'degraded',
    latency: 418,
    change: +57,
    uptime: '99.42%',
    owner: 'Infra'
  },
  {
    key: 'analytics',
    name: 'Analytics API',
    status: 'operational',
    latency: 264,
    change: -32,
    uptime: '99.88%',
    owner: 'Data'
  },
  {
    key: 'notifications',
    name: 'Notification Hub',
    status: 'maintenance',
    latency: 341,
    change: +12,
    uptime: '99.74%',
    owner: 'Messaging'
  }
]

export const adminAlertFeed = [
  {
    id: 'AL-9101',
    severity: 'high',
    title: '信用卡渠道响应延迟',
    message: 'Billing Service 峰值响应超出阈值 35%，已切换备用队列。',
    timestamp: '2025-10-04 09:42',
    acknowledged: false,
    owner: 'payments@demo.io'
  },
  {
    id: 'AL-9102',
    severity: 'medium',
    title: '批量推送计划延期',
    message: 'Notification Hub 日间批次推送耗时增加 18 分钟，自动评估中。',
    timestamp: '2025-10-04 10:18',
    acknowledged: false,
    owner: 'messaging@demo.io'
  },
  {
    id: 'AL-9103',
    severity: 'low',
    title: '报表导出重试成功',
    message: 'Analytics 导出任务第 2 次重试通过，输出文件已推送。',
    timestamp: '2025-10-04 11:06',
    acknowledged: true,
    owner: 'dataops@demo.io'
  }
]

export const adminTaskBoard = [
  {
    id: 'TASK-5021',
    title: '梳理管理员权限矩阵',
    assignee: 'Linda',
    avatarColor: '#2563eb',
    due: '2025-10-06',
    priority: 'high',
    status: 'in_progress',
    tags: ['安全', '权限']
  },
  {
    id: 'TASK-5022',
    title: '优化用户分群缓存策略',
    assignee: 'Kevin',
    avatarColor: '#0ea5e9',
    due: '2025-10-08',
    priority: 'medium',
    status: 'todo',
    tags: ['性能']
  },
  {
    id: 'TASK-5023',
    title: '对接 CRM 同步任务监控',
    assignee: 'Hiro',
    avatarColor: '#f97316',
    due: '2025-10-05',
    priority: 'high',
    status: 'in_progress',
    tags: ['集成']
  },
  {
    id: 'TASK-5024',
    title: '完善操作审计落库脚本',
    assignee: 'Alice',
    avatarColor: '#10b981',
    due: '2025-10-07',
    priority: 'low',
    status: 'review',
    tags: ['合规']
  }
]

export const adminAuditTimeline = [
  {
    id: 'AUD-3001',
    actor: '陈晨',
    action: '调整角色权限',
    target: '运营管理员',
    time: '09:12',
    status: 'success',
    detail: '新增「导出报表」权限并推送通知'
  },
  {
    id: 'AUD-3002',
    actor: 'Jacob',
    action: '创建自动化流程',
    target: '邀约短信触达',
    time: '10:05',
    status: 'success',
    detail: '流程已接入风控校验钩子'
  },
  {
    id: 'AUD-3003',
    actor: '王敏',
    action: '批量禁用账号',
    target: '休眠用户 36 人',
    time: '10:44',
    status: 'warning',
    detail: '操作需在 24 小时内复核'
  },
  {
    id: 'AUD-3004',
    actor: 'Ravi',
    action: '回滚配置',
    target: '全局缓存策略',
    time: '11:28',
    status: 'success',
    detail: '版本 3.4.1 -> 3.3.9，恢复耗时 2 分钟'
  }
]

export const adminTeamShifts = [
  {
    id: 'SHIFT-01',
    name: '晨间巡检',
    lead: 'Jessica',
    window: '08:00 - 12:00',
    coverage: 5,
    readiness: 0.92
  },
  {
    id: 'SHIFT-02',
    name: '增长热线',
    lead: 'Han',
    window: '12:00 - 18:00',
    coverage: 4,
    readiness: 0.85
  },
  {
    id: 'SHIFT-03',
    name: '夜间待命',
    lead: 'Priya',
    window: '18:00 - 24:00',
    coverage: 3,
    readiness: 0.78
  }
]
