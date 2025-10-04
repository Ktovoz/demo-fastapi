<template>
  <div class="dashboard" v-if="!loading">
    <section class="dashboard-hero">
      <div class="hero-text">
        <div class="hero-greeting">
          <span class="hero-emoji">{{ greetingEmoji }}</span>
          <span>{{ greetingText }}，{{ greetingName }}</span>
        </div>
        <h2 class="hero-title">监控全局运行态势，及时掌握后台风向</h2>
        <p class="hero-credit">由 ktovoz 倾情奉献</p>
        <p class="hero-subtitle">
          最近 7 天共处理 <strong>{{ trafficHighlights.totalRequestsDisplay }}</strong> 次 API 请求，平均活跃用户
          <strong>{{ trafficHighlights.avgUsersDisplay }}</strong> 人。快速复盘重点指标，为下一步决策做好准备。
        </p>
        <div class="hero-status">
          <a-tag color="success" :bordered="false">运行中：{{ healthSummary.operational }}/{{ healthSummary.total }}</a-tag>
          <a-tag v-if="healthSummary.degraded" color="warning" :bordered="false">待关注：{{ healthSummary.degraded }}</a-tag>
          <a-tag v-if="healthSummary.down" color="error" :bordered="false">故障：{{ healthSummary.down }}</a-tag>
        </div>
      </div>
      <div class="hero-metrics">
        <div class="hero-metric">
          <span class="hero-metric__label">本周峰值日</span>
          <span class="hero-metric__value">{{ trafficHighlights.busiestDay }}</span>
          <span class="hero-metric__hint">API 请求冲高日</span>
        </div>
        <div class="hero-metric">
          <span class="hero-metric__label">服务覆盖</span>
          <span class="hero-metric__value">{{ healthSummary.total }} 项</span>
          <span class="hero-metric__hint">包含核心与辅助服务</span>
        </div>
        <div class="hero-metric">
          <span class="hero-metric__label">状态面板</span>
          <span class="hero-metric__value">{{ healthSummary.operational }} 正常</span>
          <span class="hero-metric__hint">{{ healthSummary.degraded }} 待关注 · {{ healthSummary.down }} 故障</span>
        </div>
      </div>
    </section>

    <section class="dashboard-metrics">
      <a-row :gutter="[16, 16]">
        <a-col :xs="24" :sm="12" :xl="6" v-for="card in decoratedSummaryCards" :key="card.key">
          <CardContainer :body-padding="'18px'" :hoverable="true" :description="card.hint">
            <template #icon>
              <div class="metric-card__icon" :class="card.accentClass">
                <component :is="card.icon" />
              </div>
            </template>
            <template #title>
              <span class="metric-card__title">{{ card.title }}</span>
            </template>
            <div class="metric-card">
              <div class="metric-card__value">{{ card.value }}</div>
              <div class="metric-card__footer">
                <span class="metric-card__trend" :class="card.trendClass">
                  <component :is="card.trendIcon" />
                  {{ card.change }}
                </span>
                <span class="metric-card__badge">{{ card.trendText }}</span>
              </div>
            </div>
          </CardContainer>
        </a-col>
      </a-row>
    </section>

    <section class="dashboard-panels">
      <a-row :gutter="[16, 16]">
        <a-col :xs="24" :xl="16">
          <CardContainer
            title="流量趋势总览"
            description="按日对比 API 请求与活跃用户变化"
            :body-padding="'0'"
          >
            <template #icon>
              <div class="panel-icon panel-icon--blue">
                <BarChartOutlined />
              </div>
            </template>
            <div class="trend-panel">
              <div class="trend-legend">
                <span class="legend-dot legend-dot--primary"></span>
                <span>API Requests</span>
                <span class="legend-dot legend-dot--secondary"></span>
                <span>Active Users</span>
              </div>
              <div class="trend-grid">
                <div v-for="row in trendRows" :key="row.label" class="trend-row">
                  <div class="trend-row__label">{{ row.label }}</div>
                  <div class="trend-row__metrics">
                    <div class="trend-row__metric">
                      <span class="metric-label">{{ row.api }}</span>
                      <a-progress :percent="row.apiPercent" size="small" :show-info="false" stroke-color="#2563eb" />
                    </div>
                    <div class="trend-row__metric trend-row__metric--secondary">
                      <span class="metric-label">{{ row.users }}</span>
                      <a-progress :percent="row.usersPercent" size="small" :show-info="false" stroke-color="#06b6d4" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </CardContainer>
        </a-col>
        <a-col :xs="24" :xl="8">
          <CardContainer
            title="系统健康状态"
            description="实时同步各核心模块的运行状况"
            :body-padding="'18px'"
          >
            <template #icon>
              <div class="panel-icon panel-icon--purple">
                <FieldTimeOutlined />
              </div>
            </template>
            <div class="health-list">
              <div
                v-for="item in systemStatuses"
                :key="item.label"
                class="health-item"
                :class="`health-item--${item.status}`"
              >
                <div class="health-item__header">
                  <a-badge :status="item.badge" />
                  <span class="health-item__label">{{ item.label }}</span>
                  <a-tag v-if="item.status === 'degraded'" color="warning" :bordered="false">需关注</a-tag>
                  <a-tag v-if="item.status === 'down'" color="error" :bordered="false">故障</a-tag>
                </div>
                <p class="health-item__message">{{ item.message }}</p>
              </div>
            </div>
          </CardContainer>
        </a-col>
      </a-row>
    </section>

    <section class="dashboard-bottom">
      <a-row :gutter="[16, 16]">
        <a-col :xs="24" :lg="12">
          <CardContainer
            title="实时活动追踪"
            description="记录最近的审批与自动化事件"
            :body-padding="'18px'"
          >
            <template #icon>
              <div class="panel-icon panel-icon--green">
                <ThunderboltOutlined />
              </div>
            </template>
            <a-timeline class="activity-timeline">
              <a-timeline-item v-for="item in activityTimeline" :key="item.id" :color="item.color">
                <div class="activity-item">
                  <div class="activity-item__time">{{ item.time }}</div>
                  <div class="activity-item__body">
                    <strong>{{ item.user }}</strong>
                    <span class="activity-item__action">{{ item.action }}</span>
                    <span class="activity-item__target">{{ item.target }}</span>
                  </div>
                </div>
              </a-timeline-item>
            </a-timeline>
          </CardContainer>
        </a-col>
        <a-col :xs="24" :lg="12">
          <CardContainer
            title="快捷操作"
            description="一键处理日常高频任务"
            :body-padding="'18px'"
          >
            <template #icon>
              <div class="panel-icon panel-icon--amber">
                <ReloadOutlined />
              </div>
            </template>
            <div class="quick-actions">
              <button
                v-for="action in quickActions"
                :key="action.key"
                class="quick-action"
                :class="`quick-action--${action.tone}`"
                type="button"
                @click="action.handler()"
              >
                <span class="quick-action__icon">
                  <component :is="action.icon" />
                </span>
                <span class="quick-action__content">
                  <span class="quick-action__label">{{ action.label }}</span>
                  <span class="quick-action__description">{{ action.description }}</span>
                </span>
                <ArrowRightOutlined class="quick-action__chevron" />
              </button>
            </div>
          </CardContainer>
        </a-col>
      </a-row>
    </section>
  </div>
  <Loading v-else overlay tip="Loading dashboard" />
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import {
  ArrowUpOutlined,
  ArrowDownOutlined,
  MinusOutlined,
  TeamOutlined,
  BarChartOutlined,
  AlertOutlined,
  ClockCircleOutlined,
  FieldTimeOutlined,
  ThunderboltOutlined,
  ReloadOutlined,
  DeploymentUnitOutlined,
  ArrowRightOutlined
} from '@ant-design/icons-vue'
import { useAuthStore } from '../../store/auth'
import { dashboardApi } from '../../api/dashboard'
import CardContainer from '../../components/layout/CardContainer.vue'
import Loading from '../../components/common/Loading.vue'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const summaryCards = ref([])
const chartData = ref([])
const systemHealth = ref([])
const recentActivities = ref([])

const statusMap = {
  operational: { status: 'success', label: 'Operational' },
  degraded: { status: 'warning', label: 'Degraded' },
  down: { status: 'error', label: 'Down' }
}

const greetingName = computed(() => authStore.user?.name ?? '管理员')
const greetingText = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return '早上好'
  if (hour < 18) return '下午好'
  return '晚上好'
})
const greetingEmoji = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return '🌅'
  if (hour < 18) return '🌤️'
  return '🌙'
})

const decoratedSummaryCards = computed(() => {
  const iconMap = {
    users: TeamOutlined,
    sessions: BarChartOutlined,
    errors: AlertOutlined,
    uptime: ClockCircleOutlined
  }
  const accentMap = {
    users: 'accent-users',
    sessions: 'accent-sessions',
    errors: 'accent-errors',
    uptime: 'accent-uptime'
  }
  const trendTextMap = {
    up: '高于上周',
    down: '低于上周',
    flat: '与上周持平'
  }
  const hintMap = {
    users: '今日新增用户已同步',
    sessions: '统计来自演示环境',
    errors: '包含告警与提醒',
    uptime: '近 30 天维持高可用'
  }
  return summaryCards.value.map((card) => {
    const trendIcon = card.trend === 'up' ? ArrowUpOutlined : card.trend === 'down' ? ArrowDownOutlined : MinusOutlined
    return {
      ...card,
      icon: iconMap[card.key] ?? BarChartOutlined,
      accentClass: accentMap[card.key] ?? 'accent-generic',
      trendIcon,
      trendClass: `trend-${card.trend ?? 'flat'}`,
      trendText: trendTextMap[card.trend] ?? '数据稳定',
      hint: hintMap[card.key] ?? '自动同步 Demo 数据'
    }
  })
})

const trendRows = computed(() => {
  if (!chartData.value.length) return []
  const apiValues = chartData.value.map((row) => row.series[0])
  const userValues = chartData.value.map((row) => row.series[1])
  const maxApi = Math.max(...apiValues)
  const maxUsers = Math.max(...userValues)
  return chartData.value.map((row) => ({
    label: row.label,
    api: row.series[0],
    users: row.series[1],
    apiPercent: maxApi ? Math.round((row.series[0] / maxApi) * 100) : 0,
    usersPercent: maxUsers ? Math.round((row.series[1] / maxUsers) * 100) : 0
  }))
})

const healthSummary = computed(() => {
  const total = systemHealth.value.length
  const operational = systemHealth.value.filter((item) => item.status === 'operational').length
  const degraded = systemHealth.value.filter((item) => item.status === 'degraded').length
  const down = systemHealth.value.filter((item) => item.status === 'down').length
  return { total, operational, degraded, down }
})

const systemStatuses = computed(() =>
  systemHealth.value.map((item) => ({
    ...item,
    badge: statusMap[item.status]?.status ?? 'default'
  }))
)

const trafficHighlights = computed(() => {
  if (!chartData.value.length) {
    return {
      busiestDay: '-',
      totalRequests: 0,
      totalRequestsDisplay: '0',
      avgUsers: 0,
      avgUsersDisplay: '0'
    }
  }
  const requestValues = chartData.value.map((row) => row.series[0])
  const userValues = chartData.value.map((row) => row.series[1])
  const busiestIndex = requestValues.indexOf(Math.max(...requestValues))
  const busiestDay = chartData.value[busiestIndex]?.label ?? '-'
  const totalRequests = requestValues.reduce((sum, value) => sum + value, 0)
  const avgUsers = Math.round(userValues.reduce((sum, value) => sum + value, 0) / userValues.length)
  return {
    busiestDay,
    totalRequests,
    totalRequestsDisplay: totalRequests.toLocaleString(),
    avgUsers,
    avgUsersDisplay: avgUsers.toLocaleString()
  }
})

const activityTimeline = computed(() =>
  recentActivities.value.map((item, index) => ({
    id: item.id,
    time: item.time,
    user: item.user,
    action: item.action,
    target: item.target,
    color: index === 0 ? 'green' : index === 1 ? 'blue' : 'gray'
  }))
)

const loadMetrics = async () => {
  loading.value = true
  try {
    const response = await dashboardApi.fetchMetrics()
    const data = response.data
    summaryCards.value = data.summaryCards
    chartData.value = data.trafficChart.labels.map((label, index) => ({
      label,
      series: data.trafficChart.series.map((series) => series.data[index])
    }))
    systemHealth.value = data.systemHealth
    recentActivities.value = data.recentActivities
  } catch (error) {
    message.error('Failed to load dashboard data')
  } finally {
    loading.value = false
  }
}

const refresh = () => {
  loadMetrics()
}

const navigate = (path) => {
  router.push(path)
}

const quickActions = computed(() => [
  {
    key: 'refresh',
    label: '刷新指标',
    description: '同步最新运行状态',
    icon: ReloadOutlined,
    tone: 'primary',
    handler: refresh
  },
  {
    key: 'create-user',
    label: '创建用户',
    description: '邀请新成员加入演示环境',
    icon: TeamOutlined,
    tone: 'neutral',
    handler: () => navigate('/users/list')
  },
  {
    key: 'review-roles',
    label: '配置角色',
    description: '快速对齐权限矩阵',
    icon: DeploymentUnitOutlined,
    tone: 'neutral',
    handler: () => navigate('/roles/list')
  }
])

onMounted(loadMetrics)
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.dashboard section {
  position: relative;
  z-index: 1;
}

.dashboard-hero {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
  padding: 24px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(229, 234, 242, 0.92), rgba(210, 228, 255, 0.88));
  border: 1px solid rgba(203, 213, 225, 0.65);
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
}

.hero-text {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.hero-greeting {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 500;
  color: #2563eb;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.hero-emoji {
  font-size: 18px;
}

.hero-title {
  margin: 0;
  font-size: clamp(24px, 3.8vw, 30px);
  font-weight: 600;
  color: #0f172a;
}

.hero-credit {
  margin: 6px 0 12px;
  font-size: 12px;
  color: #94a3b8;
  letter-spacing: 0.04em;
}

.hero-subtitle {
  margin: 0;
  color: #334155;
  line-height: 1.6;
  font-size: 14px;
}

.hero-subtitle strong {
  color: #1d4ed8;
}

.hero-status {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.hero-metrics {
  display: grid;
  gap: 12px;
}

.hero-metric {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 16px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(226, 232, 240, 0.7);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

.hero-metric__label {
  font-size: 11px;
  text-transform: uppercase;
  color: #64748b;
  letter-spacing: 0.08em;
}

.hero-metric__value {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
}

.hero-metric__hint {
  font-size: 12px;
  color: #64748b;
}

.metric-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.metric-card__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 10px;
  color: #fff;
}

.metric-card__title {
  font-size: 15px;
  font-weight: 600;
  color: #0f172a;
}

.metric-card__value {
  font-size: 26px;
  font-weight: 600;
  color: #0f172a;
}

.metric-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.metric-card__trend {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-weight: 500;
  font-size: 13px;
}

.metric-card__trend.trend-up {
  color: #16a34a;
}

.metric-card__trend.trend-down {
  color: #dc2626;
}

.metric-card__trend.trend-flat {
  color: #64748b;
}

.metric-card__trend :deep(.anticon) {
  font-size: 12px;
}

.metric-card__badge {
  font-size: 12px;
  color: #64748b;
}

.accent-users {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
}

.accent-sessions {
  background: linear-gradient(135deg, #0ea5e9, #06b6d4);
}

.accent-errors {
  background: linear-gradient(135deg, #f97316, #ec4899);
}

.accent-uptime {
  background: linear-gradient(135deg, #22c55e, #16a34a);
}

.accent-generic {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
}

.dashboard-panels,
.dashboard-bottom {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.panel-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  color: #fff;
}

.panel-icon--blue {
  background: linear-gradient(135deg, #1d4ed8, #6366f1);
}

.panel-icon--purple {
  background: linear-gradient(135deg, #8b5cf6, #c084fc);
}

.panel-icon--green {
  background: linear-gradient(135deg, #16a34a, #22c55e);
}

.panel-icon--amber {
  background: linear-gradient(135deg, #f59e0b, #f97316);
}

.trend-panel {
  padding: 20px 22px;
}

.trend-legend {
  display: inline-grid;
  grid-template-columns: auto auto;
  gap: 6px 12px;
  font-size: 12px;
  color: #475569;
  margin-bottom: 14px;
  align-items: center;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.legend-dot--primary {
  background: #2563eb;
}

.legend-dot--secondary {
  background: #06b6d4;
}

.trend-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.trend-row {
  display: grid;
  grid-template-columns: 70px 1fr;
  gap: 10px;
  align-items: center;
}

.trend-row__label {
  font-weight: 600;
  color: #0f172a;
}

.trend-row__metrics {
  display: grid;
  gap: 10px;
}

.trend-row__metric {
  display: grid;
  grid-template-columns: 52px 1fr;
  gap: 10px;
  align-items: center;
}

.metric-label {
  font-size: 12px;
  color: #475569;
  font-variant-numeric: tabular-nums;
}

.trend-row__metric--secondary .metric-label {
  color: #0f766e;
}

.health-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.health-item {
  padding: 14px 16px;
  border-radius: 16px;
  border: 1px solid rgba(226, 232, 240, 0.75);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

.health-item--operational {
  border-color: rgba(34, 197, 94, 0.35);
}

.health-item--degraded {
  border-color: rgba(234, 179, 8, 0.35);
  background: rgba(254, 240, 138, 0.22);
}

.health-item--down {
  border-color: rgba(248, 113, 113, 0.35);
  background: rgba(254, 242, 242, 0.6);
}

.health-item__header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #0f172a;
}

.health-item__message {
  margin: 6px 0 0;
  font-size: 12px;
  color: #475569;
}

.activity-timeline {
  margin-top: 2px;
}

.activity-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.activity-item__time {
  font-size: 12px;
  color: #94a3b8;
  font-variant-numeric: tabular-nums;
}

.activity-item__body {
  display: inline-flex;
  flex-wrap: wrap;
  gap: 6px;
  font-size: 13px;
  color: #1f2937;
}

.activity-item__action {
  color: #0f172a;
}

.activity-item__target {
  color: #2563eb;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.quick-action {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 12px;
  align-items: center;
  padding: 14px 16px;
  border-radius: 16px;
  border: 1px solid rgba(226, 232, 240, 0.75);
  background: rgba(255, 255, 255, 0.96);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  cursor: pointer;
}

.quick-action--primary {
  border-color: rgba(37, 99, 235, 0.35);
  background: linear-gradient(135deg, rgba(219, 234, 254, 0.92), rgba(191, 219, 254, 0.86));
}

.quick-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
  border-color: rgba(59, 130, 246, 0.35);
}

.quick-action__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(37, 99, 235, 0.12);
  color: #1d4ed8;
}

.quick-action--primary .quick-action__icon {
  background: rgba(37, 99, 235, 0.2);
}

.quick-action__content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  text-align: left;
}

.quick-action__label {
  font-size: 15px;
  font-weight: 600;
  color: #0f172a;
}

.quick-action__description {
  font-size: 12px;
  color: #64748b;
}

.quick-action__chevron {
  color: #94a3b8;
}

.quick-action--neutral .quick-action__icon {
  background: rgba(148, 163, 184, 0.16);
  color: #475569;
}

@media (max-width: 992px) {
  .dashboard-hero {
    grid-template-columns: 1fr;
  }

  .hero-metrics {
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  }
}

@media (max-width: 768px) {
  .dashboard {
    gap: 20px;
  }

  .dashboard-hero {
    padding: 20px;
  }

  .trend-row {
    grid-template-columns: 1fr;
  }

  .trend-row__metric {
    grid-template-columns: 70px 1fr;
  }
}
</style>
