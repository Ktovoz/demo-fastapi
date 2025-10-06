<template>
  <div class="system-logs">
    <section class="log-summary" v-if="logSummary">
      <CardContainer
        title="日志总览"
        description="追踪近 24 小时系统日志的级别分布与模块热点"
        :body-padding="'20px'"
        :hoverable="true"
      >
        <template #icon>
          <div class="summary-icon">
            <RadarChartOutlined />
          </div>
        </template>
        <div class="summary-grid">
          <div v-for="item in severityItems" :key="item.key" class="summary-tile" :class="`severity-${item.key}`">
            <component :is="item.icon" class="summary-tile__icon" />
            <div class="summary-tile__content">
              <span class="summary-tile__label">{{ item.label }}</span>
              <strong class="summary-tile__value">{{ item.count }}</strong>
              <span class="summary-tile__hint">占比 {{ item.percent }}%</span>
            </div>
          </div>
        </div>
        <div class="summary-footer">
          <div class="summary-kpi">
            <a-badge status="processing" />
            <span>错误占比 {{ logSummary.errorRatio }}%</span>
            <a-divider type="vertical" />
            <span>总日志 {{ logSummary.total }}</span>
          </div>
          <a-space>
            <a-button type="link" size="small" @click="refreshAll">刷新数据</a-button>
          </a-space>
        </div>
      </CardContainer>
    </section>

    <section class="log-search">
      <SearchForm
        :items="searchItems"
        v-model="formValues"
        @submit="handleSearch"
        @reset="handleReset"
      >
        <template #extra>
          <a-space>
            <a-button @click="exportLogs">导出日志</a-button>
          </a-space>
        </template>
      </SearchForm>
    </section>

    <section class="log-content">
      <a-row :gutter="[16, 16]">
        <a-col :xs="24" :xl="16">
          <CardContainer
            title="日志列表"
            description="支持按级别、关键词过滤，并可按时间排序"
            :body-padding="'0'"
          >
            <template #icon>
              <div class="panel-icon panel-icon--blue">
                <BugOutlined />
              </div>
            </template>
            <div class="table-wrapper">
              <Loading v-if="combinedLoading && logs.length === 0" size="small" />
              <template v-else>
                <Table
                  :columns="columns"
                  :data-source="logs"
                  :loading="logLoading"
                  :pagination="false"
                  row-key="id"
                  @change="handleTableChange"
                >
                  <template #level="{ record }">
                    <a-tag :color="levelColor(record.level)" :bordered="false">
                      <component :is="levelMap[record.level]?.icon" v-if="levelMap[record.level]?.icon" />
                      {{ levelMap[record.level]?.label || record.level }}
                    </a-tag>
                  </template>
                  <template #user="{ record }">
                    <div v-if="record.context.userEmail">
                      <div class="user-email">{{ record.context.userEmail }}</div>
                      <div class="user-name">{{ record.context.userName || '用户' }}</div>
                    </div>
                    <span v-else class="anonymous-user">
                      <a-tag color="default" size="small">匿名用户</a-tag>
                    </span>
                  </template>
                  <template #ip="{ record }">
                    <span class="ip-address">{{ record.context.ip }}</span>
                  </template>
                  <template #message="{ record }">
                    <a-tooltip :title="record.message" placement="topLeft">
                      <a-typography-paragraph
                        class="log-message"
                        :ellipsis="{ rows: 2 }"
                        style="cursor: pointer;"
                        @click="showLogDetail(record)"
                      >
                        {{ record.message }}
                      </a-typography-paragraph>
                    </a-tooltip>
                  </template>
                </Table>
                <div class="table-footer">
                  <Pagination
                    :total="logTotal"
                    v-model:current="logPagination.page"
                    v-model:page-size="logPagination.pageSize"
                    :page-size-options="['10', '20', '50', '100']"
                    :show-size-changer="true"
                    :show-total="true"
                    :show-quick-jumper="true"
                    @change="handlePageChange"
                  />
                </div>
              </template>
            </div>
          </CardContainer>
        </a-col>
        <a-col :xs="24" :xl="8">
          <CardContainer
            title="模块热点"
            description="统计近 24 小时高频模块，帮助定位波动来源"
            :body-padding="'18px'"
          >
            <template #icon>
              <div class="panel-icon panel-icon--purple">
                <ClusterOutlined />
              </div>
            </template>
            <div class="module-list" v-if="moduleBreakdown.length">
              <div v-for="item in moduleBreakdown" :key="item.module" class="module-item">
                <div class="module-label">
                  <span>{{ item.module }}</span>
                  <span>{{ item.total }} 次</span>
                </div>
                <a-progress :percent="item.percent" :show-info="false" stroke-color="#6366f1" size="small" />
              </div>
            </div>
            <div class="empty-hint" v-else>暂无模块统计</div>
          </CardContainer>

          <CardContainer
            title="最新日志"
            description="最近六条日志的快速预览"
            :body-padding="'18px'"
            style="margin-top: 16px;"
          >
            <template #icon>
              <div class="panel-icon panel-icon--amber">
                <ClockCircleOutlined />
              </div>
            </template>
            <Loading v-if="logSummaryLoading && recentLogs.length === 0" size="small" />
            <a-timeline v-else class="recent-timeline">
              <a-timeline-item v-for="item in recentLogs" :key="item.id" :color="levelColor(item.level, true)">
                <div class="recent-item">
                  <div class="recent-item__meta">
                    <span class="recent-item__time">{{ item.time }}</span>
                    <a-tag size="small" :color="levelColor(item.level)" :bordered="false">
                      <component :is="levelMap[item.level]?.icon" v-if="levelMap[item.level]?.icon" style="font-size: 12px; margin-right: 4px;" />
                      {{ levelMap[item.level]?.label || item.level }}
                    </a-tag>
                  </div>
                  <div class="recent-item__body">
                    <div class="recent-item__header">
                      <strong>{{ item.module }}</strong>
                      <span class="recent-item__action">{{ item.action }}</span>
                    </div>
                    <p class="recent-item__description">{{ item.message }}</p>
                  </div>
                </div>
              </a-timeline-item>
            </a-timeline>
          </CardContainer>
        </a-col>
      </a-row>
    </section>

    <!-- 日志详情弹窗 -->
    <a-modal
      v-model:open="detailModalVisible"
      title="日志详情"
      width="700px"
      :footer="null"
      @cancel="closeLogDetail"
    >
      <div v-if="selectedLog" class="log-detail">
        <a-descriptions :column="2" size="small" bordered>
          <a-descriptions-item label="时间">
            {{ selectedLog.time }}
          </a-descriptions-item>
          <a-descriptions-item label="级别">
            <a-tag :color="levelColor(selectedLog.level)" :bordered="false">
              <component :is="levelMap[selectedLog.level]?.icon" v-if="levelMap[selectedLog.level]?.icon" />
              {{ levelMap[selectedLog.level]?.label || selectedLog.level }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="用户">
            <a-tag color="blue" size="small" v-if="selectedLog.context.userId">管理员</a-tag>
            <a-tag color="default" size="small" v-else>匿名</a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="模块">
            {{ selectedLog.module }}
          </a-descriptions-item>
          <a-descriptions-item label="操作" :span="2">
            {{ selectedLog.action }}
          </a-descriptions-item>
          <a-descriptions-item label="IP地址">
            {{ selectedLog.context.ip }}
          </a-descriptions-item>
          <a-descriptions-item label="用户代理">
            <a-tooltip :title="selectedLog.context.userAgent">
              <span class="user-agent-text">{{ selectedLog.context.userAgent || 'N/A' }}</span>
            </a-tooltip>
          </a-descriptions-item>
          <a-descriptions-item label="详情描述" :span="2">
            {{ selectedLog.message }}
          </a-descriptions-item>
          <a-descriptions-item label="请求ID">
            {{ selectedLog.context.requestId }}
          </a-descriptions-item>
          <a-descriptions-item label="资源">
            {{ selectedLog.context.resource || 'N/A' }}
          </a-descriptions-item>
        </a-descriptions>

        <!-- 请求数据 -->
        <div v-if="selectedLog.context" class="detail-section">
          <h4>请求数据</h4>
          <a-typography-paragraph>
            <pre>{{ formatJson(selectedLog.context) }}</pre>
          </a-typography-paragraph>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { message } from 'ant-design-vue'
import SearchForm from '../../components/common/SearchForm.vue'
import Table from '../../components/common/Table.vue'
import Pagination from '../../components/common/Pagination.vue'
import CardContainer from '../../components/layout/CardContainer.vue'
import Loading from '../../components/common/Loading.vue'
import { useSystemStore } from '../../store/system'
import {
  BugOutlined,
  ClockCircleOutlined,
  ClusterOutlined,
  ExclamationCircleOutlined,
  InfoCircleOutlined,
  RadarChartOutlined,
  WarningOutlined
} from '@ant-design/icons-vue'

const systemStore = useSystemStore()

const { logs, logTotal, logLoading, logPagination, logSummary, logSummaryLoading } = storeToRefs(systemStore)

const formValues = reactive({
  keyword: systemStore.logFilters.keyword,
  level: systemStore.logFilters.level
})

const searchItems = [
  { key: 'keyword', label: '关键词', component: 'a-input', props: { placeholder: '消息、模块或请求 ID' } },
  {
    key: 'level',
    label: '级别',
    component: 'a-select',
    props: {
      options: [
        { label: '全部', value: 'ALL' },
        { label: 'INFO', value: 'INFO' },
        { label: 'WARN', value: 'WARN' },
        { label: 'ERROR', value: 'ERROR' },
        { label: 'DEBUG', value: 'DEBUG' }
      ]
    }
  }
]

const columns = [
  {
    title: '时间',
    dataIndex: 'time',
    key: 'time',
    width: 140,
    sorter: true,
    ellipsis: true
  },
  {
    title: '用户',
    dataIndex: 'context',
    key: 'user',
    width: 150,
    slots: { customRender: 'user' },
    filters: [
      { text: '管理员', value: 'admin' },
      { text: '匿名', value: 'anonymous' }
    ],
    onFilter: (value, record) => {
      return value === 'admin' ? record.context.userId : !record.context.userId
    }
  },
  {
    title: '级别',
    dataIndex: 'level',
    key: 'level',
    width: 70,
    slots: { customRender: 'level' },
    filters: [
      { text: '错误', value: 'ERROR' },
      { text: '警告', value: 'WARN' },
      { text: '信息', value: 'INFO' },
      { text: '调试', value: 'DEBUG' }
    ],
    onFilter: (value, record) => record.level === value
  },
  {
    title: '模块',
    dataIndex: 'module',
    key: 'module',
    width: 120,
    ellipsis: true,
    filters: [
      { text: '认证系统', value: '认证系统' },
      { text: '用户管理', value: '用户管理' },
      { text: '仪表盘', value: '仪表盘' },
      { text: '系统管理', value: '系统管理' },
      { text: '角色管理', value: '角色管理' }
    ],
    onFilter: (value, record) => record.module === value
  },
  {
    title: '操作',
    dataIndex: 'action',
    key: 'action',
    width: 160,
    ellipsis: true
  },
  {
    title: 'IP地址',
    dataIndex: 'context',
    key: 'ip',
    width: 120,
    slots: { customRender: 'ip' }
  }
]

const levelMap = {
  ERROR: { color: 'red', icon: ExclamationCircleOutlined, label: '错误' },
  WARN: { color: 'orange', icon: WarningOutlined, label: '警告' },
  INFO: { color: 'blue', icon: InfoCircleOutlined, label: '信息' },
  DEBUG: { color: 'cyan', icon: InfoCircleOutlined, label: '调试' }
}

const severityItems = computed(() => {
  if (!logSummary.value) return []
  const total = logSummary.value.total || 1
  return Object.entries(logSummary.value.severity).map(([key, count]) => ({
    key,
    count,
    percent: Math.round((count / total) * 1000) / 10,
    label: levelMap[key]?.label ?? key,
    icon: levelMap[key]?.icon ?? InfoCircleOutlined
  }))
})

const moduleBreakdown = computed(() => {
  if (!logSummary.value?.topModules) return []
  const max = Math.max(...logSummary.value.topModules.map((item) => item.total)) || 1
  return logSummary.value.topModules.map((item) => ({
    ...item,
    percent: Math.round((item.total / max) * 100)
  }))
})

const recentLogs = computed(() => logSummary.value?.recent ?? [])

const combinedLoading = computed(() => logLoading.value || logSummaryLoading.value)

const handleSearch = () => {
  systemStore.setLogFilters({ ...formValues })
  systemStore.setLogPagination({ page: 1 })
  systemStore.fetchLogs().catch((error) => {
    console.error('日志加载失败:', error)
    message.error(`日志加载失败: ${error.message || '网络错误'}`)
  })
}

const handleReset = () => {
  systemStore.resetLogFilters()
  Object.assign(formValues, { keyword: '', level: 'ALL' })
  systemStore.setLogPagination({ page: 1 })
  systemStore.fetchLogs().catch((error) => {
    console.error('日志加载失败:', error)
    message.error(`日志加载失败: ${error.message || '网络错误'}`)
  })
}

const handlePageChange = ({ page, pageSize }) => {
  systemStore.setLogPagination({ page, pageSize })
  systemStore.fetchLogs().catch((error) => {
    console.error('日志加载失败:', error)
    message.error(`日志加载失败: ${error.message || '网络错误'}`)
  })
}

const handleTableChange = (pagination, filters, sorter) => {
  const { order, field } = sorter
  systemStore.setLogSorter(order ? { field, order } : null)
  systemStore.fetchLogs().catch((error) => {
    console.error('日志加载失败:', error)
    message.error(`日志加载失败: ${error.message || '网络错误'}`)
  })
}

const exportLogs = () => {
  message.success('开始导出日志（mock）')
}

const levelColor = (level, timeline = false) => {
  const normalized = level?.toUpperCase?.() ?? 'INFO'
  const mapping = levelMap[normalized]
  if (timeline) {
    switch (normalized) {
      case 'ERROR':
        return 'red'
      case 'WARN':
        return 'orange'
      default:
        return 'blue'
    }
  }
  return mapping?.color ?? 'blue'
}

const refreshAll = async () => {
  try {
    await Promise.all([
      systemStore.fetchLogSummary(),
      systemStore.fetchLogs()
    ])
    message.success('日志数据已刷新')
  } catch (error) {
    console.error('刷新失败:', error)
    message.error(`刷新失败: ${error.message || '请稍后重试'}`)
  }
}

// 日志详情弹窗
const detailModalVisible = ref(false)
const selectedLog = ref(null)

const showLogDetail = (record) => {
  selectedLog.value = record
  detailModalVisible.value = true
}

const closeLogDetail = () => {
  detailModalVisible.value = false
  selectedLog.value = null
}

const formatJson = (obj) => {
  try {
    return JSON.stringify(obj, null, 2)
  } catch (e) {
    return String(obj)
  }
}

onMounted(async () => {
  try {
    await Promise.all([
      systemStore.fetchLogSummary(),
      systemStore.fetchLogs()
    ])
  } catch (error) {
    console.error('加载系统日志失败:', error)
    message.error(`加载系统日志失败: ${error.message || '请检查网络连接'}`)
  }
})
</script>

<style scoped>
.system-logs {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.log-summary .summary-icon {
  width: 46px;
  height: 46px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #6366f1, #22d3ee);
  color: #fff;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 14px;
  margin-top: 12px;
}

.summary-tile {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: 16px;
  background: rgba(248, 250, 252, 0.8);
  border: 1px solid rgba(226, 232, 240, 0.7);
}

.summary-tile__icon {
  font-size: 24px;
  color: #1d4ed8;
}

.summary-tile__content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.summary-tile__label {
  font-size: 12px;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.summary-tile__value {
  font-size: 24px;
  color: #0f172a;
}

.summary-tile__hint {
  font-size: 12px;
  color: #64748b;
}

.summary-footer {
  margin-top: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #475569;
}

.log-search {
  position: relative;
}

.panel-icon {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  color: #fff;
}

.panel-icon--blue {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
}

.panel-icon--purple {
  background: linear-gradient(135deg, #8b5cf6, #6d28d9);
}

.panel-icon--amber {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.table-wrapper {
  padding: 18px;
}

.table-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.context-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 12px;
  color: #64748b;
}

.log-message {
  margin: 0;
  font-size: 13px;
  line-height: 1.4;
}

.ip-address {
  font-family: 'Monaco', 'Consolas', monospace;
  font-size: 12px;
  color: #64748b;
  background: rgba(100, 116, 139, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
}

.user-email {
  font-size: 12px;
  color: #1f2937;
  font-weight: 500;
}

.user-name {
  font-size: 11px;
  color: #6b7280;
  margin-top: 1px;
}

.anonymous-user {
  font-size: 12px;
  color: #9ca3af;
}

.module-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.module-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 10px 0;
}

.module-label {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #334155;
}

.recent-timeline {
  margin-top: 8px;
}

.recent-item__meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #94a3b8;
}

.recent-item__body {
  margin-top: 4px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.recent-item__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recent-item__action {
  font-size: 11px;
  color: #64748b;
  background: rgba(100, 116, 139, 0.1);
  padding: 1px 4px;
  border-radius: 3px;
}

.recent-item__description {
  margin: 0;
  font-size: 12px;
  color: #475569;
  line-height: 1.3;
}

.empty-hint {
  padding: 20px;
  text-align: center;
  color: #94a3b8;
  font-size: 13px;
}

.log-detail .detail-section {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.log-detail .detail-section h4 {
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
}

.log-detail .detail-section pre {
  background: #f9fafb;
  padding: 12px;
  border-radius: 6px;
  font-size: 12px;
  line-height: 1.4;
  color: #374151;
  overflow-x: auto;
  max-height: 200px;
  overflow-y: auto;
}

.log-detail .user-agent-text {
  font-family: 'Monaco', 'Consolas', monospace;
  font-size: 11px;
  color: #6b7280;
  background: #f3f4f6;
  padding: 2px 4px;
  border-radius: 3px;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: inline-block;
}

@media (max-width: 768px) {
  .summary-grid {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  }

  .table-wrapper {
    padding: 12px;
  }
}
</style>

