<template>
  <div class="admin-overview">
    <Loading
      v-if="isInitializing"
      overlay
      tip="加载后台管理驾驶舱数据"
    />

    <template v-else>
      <section class="overview-hero">
        <div class="hero-copy">
          <div class="hero-badge">Operations Control • {{ todayText }}</div>
          <h2>后台管理驾驶舱</h2>
          <p>
            通过统一视图掌控活跃用户、接口健康与跨团队协同进度。
            最新请求峰值达到 <strong>{{ latestTrend?.requests.toLocaleString?.() }}</strong> 次，
            活跃用户维持在 <strong>{{ latestTrend?.activeUsers }}</strong> 人水位。
          </p>
          <div class="hero-tags">
            <a-tag color="blue" :bordered="false">服务监控 {{ overview?.services.length ?? 0 }}</a-tag>
            <a-tag color="green" :bordered="false">运营班次 {{ overview?.shifts.length ?? 0 }}</a-tag>
            <a-tag color="gold" :bordered="false">待处理告警 {{ pendingAlerts }}</a-tag>
          </div>
        </div>
        <div class="hero-visual" v-if="overview">
          <div class="trend-preview">
            <div class="trend-preview__header">
              <span>七日趋势</span>
              <strong>{{ totalRequestsDisplay }}</strong>
            </div>
            <div class="trend-preview__body">
              <div v-for="row in sparklineRows" :key="row.date" class="sparkline-row">
                <span class="sparkline-row__date">{{ row.date }}</span>
                <div class="sparkline-row__bars">
                  <span class="sparkline-bar sparkline-bar--requests" :style="{ width: row.requestWidth }"></span>
                  <span class="sparkline-bar sparkline-bar--users" :style="{ width: row.userWidth }"></span>
                </div>
                <span class="sparkline-row__error">{{ row.errorRate }}%</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="overview-cards" v-if="overview">
        <a-row :gutter="[16, 16]">
          <a-col :xs="24" :md="12" :xl="6" v-for="card in decoratedCards" :key="card.key">
            <CardContainer :body-padding="'20px'" :hoverable="true">
              <template #icon>
                <div class="metric-icon" :class="card.accent">
                  <component :is="card.icon" />
                </div>
              </template>
              <template #title>
                <span class="metric-title">{{ card.title }}</span>
              </template>
              <div class="metric-value">
                <span class="metric-number">
                  {{ card.displayValue }}<small v-if="card.unit">{{ card.unit }}</small>
                </span>
              </div>
              <div class="metric-footer">
                <span class="metric-change" :class="card.changeClass">
                  <component :is="card.changeIcon" />
                  {{ card.change }}
                </span>
                <span class="metric-hint">{{ card.trendLabel }}</span>
              </div>
              <p class="metric-description">{{ card.description }}</p>
            </CardContainer>
          </a-col>
        </a-row>
      </section>

      <section class="overview-main" v-if="overview">
        <a-row :gutter="[16, 16]">
          <a-col :xs="24" :xl="16">
            <CardContainer
              title="运行态势"
              description="汇总七日请求量、活跃用户与错误占比，辅助判断是否需要扩容或调度"
              :body-padding="'0'"
              :collapsible="false"
            >
              <template #icon>
                <div class="panel-icon panel-icon--blue">
                  <BarChartOutlined />
                </div>
              </template>
              <div class="trend-table">
                <div class="trend-table__header">
                  <span>日期</span>
                  <span>请求量</span>
                  <span>活跃用户</span>
                  <span>错误率</span>
                </div>
                <div v-for="row in trendRows" :key="row.date" class="trend-table__row">
                  <span class="trend-date">{{ row.date }}</span>
                  <div class="trend-metric">
                    <span class="trend-value">{{ row.requests.toLocaleString() }}</span>
                    <div class="trend-bar trend-bar--requests">
                      <span :style="{ width: row.requestWidth }"></span>
                    </div>
                  </div>
                  <div class="trend-metric">
                    <span class="trend-value">{{ row.activeUsers }}</span>
                    <div class="trend-bar trend-bar--users">
                      <span :style="{ width: row.userWidth }"></span>
                    </div>
                  </div>
                  <div class="trend-metric trend-metric--error">
                    <a-progress
                      :percent="row.errorPercent"
                      stroke-color="#ef4444"
                      size="small"
                      :show-info="false"
                    />
                    <span class="trend-error">{{ row.errorRate }}%</span>
                  </div>
                </div>
              </div>
            </CardContainer>
          </a-col>
          <a-col :xs="24" :xl="8">
            <CardContainer
              title="实时告警"
              description="关注进行中的运营告警，优先处理高优级别问题"
              :body-padding="'0'"
            >
              <template #icon>
                <div class="panel-icon panel-icon--amber">
                  <AlertOutlined />
                </div>
              </template>
              <div class="alert-list" :class="{ 'is-loading': alertsLoading }">
                <Loading v-if="alertsLoading && alerts.length === 0" size="small" />
                <template v-else>
                  <div v-for="alert in alerts" :key="alert.id" class="alert-item" :class="`alert-${alert.severity}`">
                    <div class="alert-head">
                      <span class="alert-id">{{ alert.id }}</span>
                      <a-tag :color="severityColor(alert.severity)" :bordered="false">{{ severityText(alert.severity) }}</a-tag>
                    </div>
                    <h4>{{ alert.title }}</h4>
                    <p>{{ alert.message }}</p>
                    <div class="alert-meta">
                      <span>{{ alert.timestamp }}</span>
                      <span>{{ alert.owner }}</span>
                    </div>
                    <a-space>
                      <a-button type="link" size="small" :disabled="alert.acknowledged" @click="acknowledge(alert.id)">
                        {{ alert.acknowledged ? '已确认' : '标记已处理' }}
                      </a-button>
                    </a-space>
                  </div>
                  <div v-if="alerts.length === 0" class="empty-hint">暂无未处理告警</div>
                </template>
              </div>
            </CardContainer>
          </a-col>
        </a-row>
      </section>

      <section class="overview-services" v-if="serviceRows.length">
        <a-row :gutter="[16, 16]">
          <a-col :xs="24" :xl="16">
            <CardContainer
              title="服务健康追踪"
              description="聚焦核心后台服务的实时状态，跟踪延迟波动与 SLA"
              :body-padding="'0'"
            >
              <template #icon>
                <div class="panel-icon panel-icon--sky">
                  <ApiOutlined />
                </div>
              </template>
              <div class="service-table">
                <div class="service-table__header">
                  <span>服务</span>
                  <span>延迟</span>
                  <span>波动</span>
                  <span>可用率</span>
                  <span>负责人</span>
                </div>
                <div v-for="service in serviceRows" :key="service.key" class="service-table__row">
                  <div class="service-name">
                    <a-badge :status="service.statusBadge" />
                    <div class="service-name__body">
                      <strong>{{ service.name }}</strong>
                      <span class="service-name__status" :class="service.statusAccent">{{ service.statusLabel }}</span>
                    </div>
                  </div>
                  <div class="service-latency">
                    <span class="service-latency__value">{{ service.latency }} ms</span>
                    <a-progress
                      :percent="service.latencyPercent"
                      size="small"
                      :show-info="false"
                      stroke-color="#2563eb"
                    />
                  </div>
                  <span class="service-change" :class="service.changeClass">
                    <component :is="service.changeIcon" />
                    {{ service.changeLabel }}
                  </span>
                  <span class="service-uptime">{{ service.uptime }}</span>
                  <span class="service-owner">{{ service.owner }}</span>
                </div>
              </div>
            </CardContainer>
          </a-col>
          <a-col :xs="24" :xl="8">
            <CardContainer
              title="状态分布"
              description="统计运行情况、可用率与团队覆盖"
              :body-padding="'20px'"
            >
              <template #icon>
                <div class="panel-icon panel-icon--teal">
                  <DeploymentUnitOutlined />
                </div>
              </template>
              <div class="service-summary">
                <div class="service-summary__headline">
                  <h3>{{ serviceSummary.total }}</h3>
                  <span>接入服务总计</span>
                </div>
                <div class="service-summary__counts">
                  <div
                    v-for="item in serviceStatusBreakdown"
                    :key="item.key"
                    class="service-summary__count"
                    :class="`is-${item.key}`"
                  >
                    <span class="service-summary__count-number">{{ item.count }}</span>
                    <span class="service-summary__count-label">{{ item.label }}</span>
                  </div>
                </div>
                <div class="service-summary__progress">
                  <div class="service-summary__progress-item">
                    <span>正常率</span>
                    <a-progress
                      :percent="serviceSummary.operationalRate"
                      status="active"
                      stroke-color="#22c55e"
                      :show-info="false"
                    />
                  </div>
                  <div class="service-summary__progress-item">
                    <span>降级率</span>
                    <a-progress
                      :percent="serviceSummary.degradedRate"
                      stroke-color="#f97316"
                      :show-info="false"
                    />
                  </div>
                  <div class="service-summary__meta">
                    <span>平均可用率</span>
                    <strong>{{ serviceSummary.averageUptime }}%</strong>
                  </div>
                </div>
                <div class="service-summary__owners" v-if="serviceSummary.owners.length">
                  <h4>团队覆盖</h4>
                  <div v-for="owner in serviceSummary.owners" :key="owner.name" class="service-summary__owner">
                    <span>{{ owner.name }}</span>
                    <a-tag color="blue" :bordered="false">{{ owner.count }}</a-tag>
                  </div>
                </div>
              </div>
            </CardContainer>
          </a-col>
        </a-row>
      </section>

      <section class="overview-bottom" v-if="overview">
        <a-row :gutter="[16, 16]">
          <a-col :xs="24" :xl="14">
            <CardContainer
              title="跨团队任务板"
              description="追踪后台管理相关的关键行动项，保持交付节奏"
              :body-padding="'0'"
            >
              <template #icon>
                <div class="panel-icon panel-icon--purple">
                  <ProjectOutlined />
                </div>
              </template>
              <div class="task-toolbar">
                <div class="task-filters">
                  <a-tag :bordered="false" color="blue">总计 {{ taskTotal }}</a-tag>
                  <a-tag :bordered="false" color="green">进行中 {{ inProgressCount }}</a-tag>
                </div>
                <a-button type="link" size="small" @click="refreshTasks">刷新</a-button>
              </div>
              <div class="task-list">
                <Loading v-if="taskLoading && tasks.length === 0" size="small" />
                <template v-else>
                  <div v-for="task in tasks" :key="task.id" class="task-card">
                    <div class="task-card__header">
                      <div class="task-avatar" :style="{ backgroundColor: task.avatarColor }">
                        {{ task.assignee.charAt(0) }}
                      </div>
                      <div class="task-info">
                        <h4>{{ task.title }}</h4>
                        <div class="task-meta">
                          <span>{{ task.assignee }}</span>
                          <span>截止 {{ task.due }}</span>
                          <a-tag size="small" :color="priorityColor(task.priority)" :bordered="false">
                            {{ priorityText(task.priority) }}
                          </a-tag>
                        </div>
                      </div>
                      <a-dropdown>
                        <template #overlay>
                          <a-menu>
                            <a-menu-item v-for="option in statusOptions" :key="option.value" @click="() => changeTaskStatus(task, option.value)">
                              {{ option.label }}
                            </a-menu-item>
                          </a-menu>
                        </template>
                        <a-button size="small" type="text">
                          {{ statusText(task.status) }}
                          <DownOutlined />
                        </a-button>
                      </a-dropdown>
                    </div>
                    <div class="task-tags">
                      <a-tag v-for="tag in task.tags" :key="tag" :bordered="false">{{ tag }}</a-tag>
                    </div>
                  </div>
                  <div v-if="tasks.length === 0" class="empty-hint">暂无任务</div>
                </template>
              </div>
              <div class="task-footer">
                <a-button type="primary" size="small" @click="quickAddTask">快速新建</a-button>
              </div>
            </CardContainer>
          </a-col>
          <a-col :xs="24" :xl="10">
            <CardContainer
              title="操作审计"
              description="记录今日后台敏感操作，辅助追踪责任人"
              :body-padding="'18px'"
            >
              <template #icon>
                <div class="panel-icon panel-icon--green">
                  <SafetyCertificateOutlined />
                </div>
              </template>
              <Loading v-if="timelineLoading && timeline.length === 0" size="small" />
              <a-timeline v-else class="audit-timeline">
                <a-timeline-item v-for="item in timeline" :key="item.id" :color="timelineColor(item.status)">
                  <div class="timeline-item">
                    <div class="timeline-item__time">{{ item.time }}</div>
                    <div class="timeline-item__body">
                      <strong>{{ item.actor }}</strong>
                      <span class="timeline-item__action">{{ item.action }}</span>
                      <span class="timeline-item__target">{{ item.target }}</span>
                      <p>{{ item.detail }}</p>
                    </div>
                  </div>
                </a-timeline-item>
              </a-timeline>
              <div class="shift-board" v-if="overview?.shifts?.length">
                <h4>今日值班</h4>
                <div class="shift-item" v-for="shift in overview.shifts" :key="shift.id">
                  <div>
                    <strong>{{ shift.name }}</strong>
                    <span>{{ shift.window }}</span>
                  </div>
                  <div class="shift-meta">
                    <span>{{ shift.lead }}</span>
                    <a-progress
                      :percent="Math.round(shift.readiness * 100)"
                      stroke-color="#22c55e"
                      size="small"
                      :show-info="false"
                    />
                  </div>
                </div>
              </div>
            </CardContainer>
          </a-col>
        </a-row>
      </section>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import {
  AlertOutlined,
  ApartmentOutlined,
  ArrowDownOutlined,
  ArrowUpOutlined,
  BarChartOutlined,
  DashboardOutlined,
  DownOutlined,
  MinusOutlined,
  ProjectOutlined,
  RiseOutlined,
  SafetyCertificateOutlined,
  TeamOutlined,
  ApiOutlined,
  DeploymentUnitOutlined
} from '@ant-design/icons-vue'
import CardContainer from '../../components/layout/CardContainer.vue'
import Loading from '../../components/common/Loading.vue'
import { useAdminStore } from '../../store/admin'

const adminStore = useAdminStore()

const statusOptions = [
  { label: '待开始', value: 'todo' },
  { label: '进行中', value: 'in_progress' },
  { label: '待确认', value: 'review' },
  { label: '已完成', value: 'done' }
]

const serviceStatusMeta = {
  operational: { badge: 'success', label: '正常', accent: 'service-status--operational' },
  degraded: { badge: 'warning', label: '性能下降', accent: 'service-status--degraded' },
  maintenance: { badge: 'processing', label: '维护中', accent: 'service-status--maintenance' },
  down: { badge: 'error', label: '故障', accent: 'service-status--down' }
}

const parsePercentage = (value) => {
  if (typeof value === 'number') {
    return value
  }
  if (typeof value !== 'string') {
    return 0
  }
  const match = value.match(/[\d.]+/)
  return match ? Number(match[0]) : 0
}

const iconMap = {
  TeamOutlined,
  RiseOutlined,
  DashboardOutlined,
  AlertOutlined
}

const trendIcons = {
  up: ArrowUpOutlined,
  down: ArrowDownOutlined
}

const todayText = new Date().toLocaleDateString('zh-CN', {
  month: '2-digit',
  day: '2-digit'
})

const overview = computed(() => adminStore.overview)
const alerts = computed(() => adminStore.alerts)
const alertsLoading = computed(() => adminStore.alertsLoading)
const tasks = computed(() => adminStore.tasks)
const taskTotal = computed(() => adminStore.taskTotal)
const taskLoading = computed(() => adminStore.taskLoading)
const timeline = computed(() => adminStore.timeline)
const timelineLoading = computed(() => adminStore.timelineLoading)

const isInitializing = computed(() => adminStore.overviewLoading && !adminStore.overview)

const latestTrend = computed(() => overview.value?.trend?.[overview.value.trend.length - 1] ?? null)

const pendingAlerts = computed(() => alerts.value.filter((item) => !item.acknowledged).length)

const decoratedCards = computed(() => {
  if (!overview.value?.cards) return []
  return overview.value.cards.map((card) => {
    const Icon = iconMap[card.icon] ?? ApartmentOutlined
    const changeIcon = trendIcons[card.changeType === 'down' ? 'down' : 'up']
    const accent = `metric-icon--${card.key}`

    return {
      ...card,
      icon: Icon,
      changeIcon,
      changeClass: card.changeType === 'down' ? 'down' : 'up',
      accent,
      displayValue: card.value.toLocaleString?.() ?? card.value
    }
  })
})

const totalRequestsDisplay = computed(() => {
  const total = overview.value?.trend?.reduce((sum, item) => sum + (item.requests || 0), 0) ?? 0
  return total.toLocaleString()
})

const sparklineRows = computed(() => {
  if (!overview.value?.trend?.length) return []
  const maxRequests = Math.max(...overview.value.trend.map((item) => item.requests)) || 1
  const maxUsers = Math.max(...overview.value.trend.map((item) => item.activeUsers)) || 1
  return overview.value.trend.map((item) => ({
    date: item.date,
    requestWidth: `${Math.round((item.requests / maxRequests) * 100)}%`,
    userWidth: `${Math.round((item.activeUsers / maxUsers) * 100)}%`,
    errorRate: item.errorRate
  }))
})

const trendRows = computed(() => {
  if (!overview.value?.trend) return []
  const maxRequests = Math.max(...overview.value.trend.map((row) => row.requests)) || 1
  const maxUsers = Math.max(...overview.value.trend.map((row) => row.activeUsers)) || 1
  return overview.value.trend.map((row) => ({
    ...row,
    requestWidth: `${Math.round((row.requests / maxRequests) * 100)}%`,
    userWidth: `${Math.round((row.activeUsers / maxUsers) * 100)}%`,
    errorPercent: Math.min(Math.round(row.errorRate * 10) / 10, 100)
  }))
})

const serviceRows = computed(() => {
  const services = overview.value?.services ?? []
  if (!services.length) return []
  const maxLatency = Math.max(...services.map((item) => item.latency ?? 0)) || 1

  return services.map((service) => {
    const status = service.status ?? 'operational'
    const meta = serviceStatusMeta[status] ?? serviceStatusMeta.operational
    const latency = Number(service.latency ?? 0)
    const latencyPercent = Math.max(0, Math.min(100, Math.round((latency / maxLatency) * 100)))
    const change = Number(service.change ?? 0)
    const changeLabel = (change > 0 ? '+' : '') + change + 'ms'
    const changeClass = change > 0 ? 'service-change--up' : change < 0 ? 'service-change--down' : 'service-change--flat'
    const changeIcon = change > 0 ? ArrowUpOutlined : change < 0 ? ArrowDownOutlined : MinusOutlined
    const uptimeValue = parsePercentage(service.uptime)

    return {
      ...service,
      status,
      statusBadge: meta.badge,
      statusLabel: meta.label,
      statusAccent: meta.accent,
      latency,
      latencyPercent,
      changeLabel,
      changeClass,
      changeIcon,
      uptimeValue
    }
  })
})

const serviceSummary = computed(() => {
  const rows = serviceRows.value
  if (!rows.length) {
    return {
      total: 0,
      counts: { operational: 0, degraded: 0, maintenance: 0, down: 0 },
      operationalRate: 0,
      degradedRate: 0,
      averageUptime: 0,
      owners: []
    }
  }

  const counts = { operational: 0, degraded: 0, maintenance: 0, down: 0 }
  let uptimeSum = 0
  const ownersMap = new Map()

  rows.forEach((service) => {
    const status = service.status ?? 'operational'
    counts[status] = (counts[status] ?? 0) + 1
    uptimeSum += service.uptimeValue ?? 0
    if (service.owner) {
      ownersMap.set(service.owner, (ownersMap.get(service.owner) ?? 0) + 1)
    }
  })

  const total = rows.length
  const operationalRate = Math.min(100, Math.round((counts.operational / total) * 100))
  const degradedRate = Math.min(100, Math.round((counts.degraded / total) * 100))
  const averageUptime = Math.round((uptimeSum / total) * 10) / 10
  const owners = Array.from(ownersMap.entries())
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)

  return {
    total,
    counts,
    operationalRate,
    degradedRate,
    averageUptime,
    owners
  }
})

const serviceStatusBreakdown = computed(() => {
  const summary = serviceSummary.value
  const order = [
    { key: 'operational', label: '正常' },
    { key: 'degraded', label: '性能下降' },
    { key: 'maintenance', label: '维护中' },
    { key: 'down', label: '故障' }
  ]

  return order.map((item) => ({
    ...item,
    count: summary.counts[item.key] ?? 0
  }))
})

const inProgressCount = computed(() => tasks.value.filter((item) => item.status === 'in_progress').length)

const severityColor = (level) => {
  switch (level) {
    case 'high':
      return 'red'
    case 'medium':
      return 'orange'
    default:
      return 'blue'
  }
}

const severityText = (level) => {
  switch (level) {
    case 'high':
      return '高'
    case 'medium':
      return '中'
    default:
      return '低'
  }
}

const statusText = (status) => {
  switch (status) {
    case 'todo':
      return '待开始'
    case 'in_progress':
      return '进行中'
    case 'review':
      return '待确认'
    case 'done':
      return '已完成'
    default:
      return status
  }
}

const priorityText = (priority) => {
  switch (priority) {
    case 'high':
      return '高优'
    case 'medium':
      return '中优'
    case 'low':
      return '低优'
    default:
      return priority
  }
}

const priorityColor = (priority) => {
  switch (priority) {
    case 'high':
      return 'red'
    case 'medium':
      return 'orange'
    default:
      return 'blue'
  }
}

const timelineColor = (status) => {
  switch (status) {
    case 'warning':
      return 'orange'
    case 'failed':
      return 'red'
    default:
      return 'green'
  }
}

const acknowledge = async (id) => {
  try {
    await adminStore.acknowledgeAlert(id)
    message.success('已标记告警为已处理')
  } catch (error) {
    message.error('操作失败，稍后重试')
  }
}

const changeTaskStatus = async (task, status) => {
  if (task.status === status) return
  try {
    await adminStore.updateTask(task.id, { status })
    message.success('任务状态已更新')
  } catch (error) {
    message.error('更新失败，请稍后再试')
  }
}

const quickAddTask = async () => {
  try {
    const payload = {
      title: '快速巡检项',
      assignee: '待分配',
      priority: 'medium',
      status: 'todo',
      tags: ['快速'],
      avatarColor: '#6366f1'
    }
    await adminStore.createTask(payload)
    message.success('已创建任务草稿')
  } catch (error) {
    message.error('创建失败')
  }
}

const refreshTasks = () => {
  adminStore.fetchTasks()
}

onMounted(async () => {
  try {
    await Promise.all([
      adminStore.fetchOverview(),
      adminStore.fetchAlerts(),
      adminStore.fetchTasks(),
      adminStore.fetchTimeline()
    ])
  } catch (error) {
    message.error('加载后台管理数据失败，请稍后刷新')
  }
})
</script>

<style scoped>
.admin-overview {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.overview-hero {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  padding: 28px;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.12), rgba(14, 165, 233, 0.08));
  border: 1px solid rgba(148, 163, 184, 0.35);
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.12);
}

.hero-copy {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.hero-badge {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #1e3a8a;
  background: rgba(59, 130, 246, 0.14);
  padding: 6px 12px;
  border-radius: 999px;
  width: fit-content;
}

.hero-copy h2 {
  margin: 0;
  font-size: clamp(26px, 4vw, 32px);
  color: #0f172a;
}

.hero-copy p {
  margin: 0;
  font-size: 14px;
  line-height: 1.8;
  color: #1f2937;
  max-width: 520px;
}

.hero-copy strong {
  color: #0f172a;
}

.hero-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.hero-visual {
  display: flex;
  align-items: center;
  justify-content: center;
}

.trend-preview {
  width: 100%;
  max-width: 340px;
  padding: 18px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(226, 232, 240, 0.6);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.trend-preview__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #1e293b;
}

.sparkline-row {
  display: grid;
  grid-template-columns: 64px 1fr 48px;
  gap: 12px;
  align-items: center;
  margin-bottom: 8px;
}

.sparkline-row__date {
  font-size: 12px;
  color: #475569;
}

.sparkline-row__bars {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sparkline-bar {
  height: 6px;
  border-radius: 999px;
  display: block;
}

.sparkline-bar--requests {
  background: linear-gradient(90deg, #2563eb, #38bdf8);
}

.sparkline-bar--users {
  background: linear-gradient(90deg, #10b981, #22d3ee);
}

.sparkline-row__error {
  font-size: 12px;
  color: #ef4444;
  text-align: right;
}

.metric-icon {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  font-size: 20px;
  color: #fff;
}

.metric-icon--activeUsers {
  background: linear-gradient(135deg, #2563eb, #60a5fa);
}

.metric-icon--conversionRate {
  background: linear-gradient(135deg, #f59e0b, #f97316);
}

.metric-icon--avgLatency {
  background: linear-gradient(135deg, #10b981, #34d399);
}

.metric-icon--escalations {
  background: linear-gradient(135deg, #ef4444, #f87171);
}

.metric-title {
  font-size: 14px;
  color: #475569;
}

.metric-value {
  margin-top: 12px;
}

.metric-number {
  font-size: 28px;
  font-weight: 600;
  color: #0f172a;
}

.metric-number small {
  font-size: 16px;
  margin-left: 4px;
  color: #475569;
}

.metric-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  font-size: 12px;
  color: #64748b;
}

.metric-change {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-weight: 600;
}

.metric-change.up {
  color: #16a34a;
}

.metric-change.down {
  color: #dc2626;
}

.metric-description {
  margin: 12px 0 0;
  font-size: 12px;
  color: #6b7280;
}

.panel-icon {
  width: 46px;
  height: 46px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  color: #fff;
}

.panel-icon--blue {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
}

.panel-icon--amber {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.panel-icon--purple {
  background: linear-gradient(135deg, #8b5cf6, #6d28d9);
}

.panel-icon--green {
  background: linear-gradient(135deg, #22c55e, #16a34a);
}

.trend-table {
  padding: 8px 12px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.trend-table__header,
.trend-table__row {
  display: grid;
  grid-template-columns: 120px repeat(3, 1fr);
  align-items: center;
  gap: 16px;
}

.trend-table__header {
  font-size: 12px;
  text-transform: uppercase;
  font-weight: 600;
  color: #64748b;
}

.trend-table__row {
  padding: 12px;
  border-radius: 12px;
  background: rgba(248, 250, 252, 0.8);
}

.trend-metric {
  display: flex;
  align-items: center;
  gap: 12px;
}

.trend-bar {
  flex: 1;
  height: 6px;
  border-radius: 999px;
  background: rgba(226, 232, 240, 0.7);
  position: relative;
  overflow: hidden;
}

.trend-bar span {
  position: absolute;
  inset: 0;
  border-radius: 999px;
}

.trend-bar--requests span {
  background: linear-gradient(90deg, #2563eb, #38bdf8);
}

.trend-bar--users span {
  background: linear-gradient(90deg, #10b981, #22d3ee);
}

.trend-error {
  font-size: 12px;
  color: #dc2626;
  width: 48px;
  text-align: right;
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 18px;
}

.alert-item {
  border-radius: 14px;
  padding: 16px;
  border: 1px solid rgba(226, 232, 240, 0.7);
  background: rgba(255, 255, 255, 0.92);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.alert-item h4 {
  margin: 0;
  font-size: 15px;
  color: #0f172a;
}

.alert-item p {
  margin: 0;
  font-size: 12px;
  color: #475569;
}

.alert-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: #334155;
}

.alert-meta {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #94a3b8;
}

.alert-high {
  border-color: rgba(248, 113, 113, 0.4);
}

.alert-medium {
  border-color: rgba(251, 191, 36, 0.4);
}

.alert-low {
  border-color: rgba(96, 165, 250, 0.4);
}

.task-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0 20px 20px;
}

.task-card {
  border-radius: 16px;
  border: 1px solid rgba(226, 232, 240, 0.7);
  padding: 16px;
  background: rgba(248, 250, 252, 0.8);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-card__header {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 12px;
  align-items: center;
}

.task-avatar {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  font-weight: 600;
  color: #fff;
}

.task-info h4 {
  margin: 0 0 4px;
  font-size: 15px;
}

.task-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #64748b;
}

.task-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.task-footer {
  padding: 0 20px 20px;
}

.audit-timeline {
  margin-bottom: 16px;
}

.timeline-item {
  display: flex;
  gap: 12px;
}

.timeline-item__time {
  font-size: 12px;
  color: #94a3b8;
  width: 48px;
}

.timeline-item__body {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.timeline-item__action {
  margin-left: 6px;
  color: #334155;
}

.timeline-item__target {
  margin-left: 6px;
  color: #0f172a;
  font-weight: 600;
}

.timeline-item__body p {
  margin: 0;
  color: #64748b;
  font-size: 12px;
}

.shift-board {
  margin-top: 16px;
  padding: 16px;
  border-radius: 14px;
  background: rgba(226, 232, 240, 0.45);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.shift-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.shift-item span {
  display: block;
  font-size: 12px;
  color: #475569;
}

.shift-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.empty-hint {
  padding: 24px;
  text-align: center;
  color: #94a3b8;
  font-size: 13px;
}

.overview-services {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.service-table {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.service-table__header,
.service-table__row {
  display: grid;
  grid-template-columns: minmax(0, 1.8fr) minmax(0, 1.1fr) minmax(0, 0.9fr) minmax(0, 0.8fr) minmax(0, 0.9fr);
  gap: 16px;
  align-items: center;
}

.service-table__header {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #64748b;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(226, 232, 240, 0.7);
}

.service-table__row {
  padding: 14px 0;
  border-bottom: 1px solid rgba(226, 232, 240, 0.6);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.service-table__row:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.service-table__row:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
}

.service-name {
  display: flex;
  align-items: center;
  gap: 12px;
}

.service-name__body {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.service-name__body strong {
  font-size: 14px;
  color: #0f172a;
}

.service-name__status {
  font-size: 12px;
  color: #64748b;
}

.service-status--operational {
  color: #16a34a;
}

.service-status--degraded {
  color: #f97316;
}

.service-status--maintenance {
  color: #0ea5e9;
}

.service-status--down {
  color: #ef4444;
}

.service-latency {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.service-latency__value {
  font-weight: 600;
  color: #0f172a;
}

.service-change {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  font-size: 13px;
}

.service-change svg {
  font-size: 12px;
}

.service-change--up {
  color: #16a34a;
}

.service-change--down {
  color: #ef4444;
}

.service-change--flat {
  color: #64748b;
}

.service-uptime {
  font-weight: 600;
  color: #111827;
}

.service-owner {
  color: #475569;
  font-size: 13px;
}

.service-summary {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.service-summary__headline {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.service-summary__headline h3 {
  margin: 0;
  font-size: 36px;
  color: #0f172a;
  line-height: 1;
}

.service-summary__headline span {
  font-size: 12px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.service-summary__counts {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.service-summary__count {
  border-radius: 14px;
  padding: 12px;
  background: rgba(226, 232, 240, 0.5);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.service-summary__count-number {
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
}

.service-summary__count-label {
  font-size: 12px;
  color: #64748b;
}

.service-summary__count.is-operational {
  background: rgba(34, 197, 94, 0.14);
}

.service-summary__count.is-degraded {
  background: rgba(249, 115, 22, 0.14);
}

.service-summary__count.is-maintenance {
  background: rgba(14, 165, 233, 0.14);
}

.service-summary__count.is-down {
  background: rgba(239, 68, 68, 0.14);
}

.service-summary__progress {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.service-summary__progress-item span {
  font-size: 12px;
  color: #64748b;
  margin-bottom: 6px;
  display: block;
}

.service-summary__meta {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 12px;
  border-radius: 12px;
  background: rgba(148, 163, 184, 0.12);
  font-size: 13px;
  color: #475569;
}

.service-summary__meta strong {
  font-size: 20px;
  color: #0f172a;
}

.service-summary__owners {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.service-summary__owners h4 {
  margin: 0;
  font-size: 13px;
  color: #334155;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.service-summary__owner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: #0f172a;
}

.panel-icon--sky {
  background: linear-gradient(140deg, rgba(14, 165, 233, 0.22), rgba(37, 99, 235, 0.22));
  color: #0f172a;
}

.panel-icon--teal {
  background: linear-gradient(140deg, rgba(45, 212, 191, 0.22), rgba(15, 118, 110, 0.22));
  color: #0f172a;
}


@media (max-width: 768px) {
  .service-table {
    padding: 16px;
  }

  .service-table__header {
    display: none;
  }

  .service-table__row {
    grid-template-columns: 1fr;
    gap: 12px;
    padding: 16px 0;
  }

  .service-latency {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }

  .service-change,
  .service-uptime,
  .service-owner {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .service-summary__counts {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }


  .trend-table__header,
  .trend-table__row {
    grid-template-columns: 100px repeat(3, minmax(0, 1fr));
    gap: 12px;
  }

  .task-card__header {
    grid-template-columns: auto 1fr;
  }

  .task-card__header > .ant-dropdown-button,
  .task-card__header > button {
    grid-column: span 2;
    justify-self: flex-start;
  }
}
</style>



