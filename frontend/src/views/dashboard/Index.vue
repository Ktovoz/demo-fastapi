<template>
  <div class="dashboard" v-if="!loading">
    <a-row :gutter="16">
      <a-col :span="6" v-for="card in summaryCards" :key="card.key">
        <CardContainer :title="card.title" bordered>
          <div class="metric-value">{{ card.value }}</div>
          <div class="metric-change" :class="card.trend">{{ card.change }}</div>
        </CardContainer>
      </a-col>
    </a-row>

    <a-row :gutter="16" style="margin-top: 16px;">
      <a-col :span="16">
        <CardContainer title="Weekly Trend" bordered collapsible>
          <a-table
            :columns="chartColumns"
            :data-source="chartRows"
            :pagination="false"
            size="small"
            row-key="label"
          />
        </CardContainer>
      </a-col>
      <a-col :span="8">
        <CardContainer title="System Health" bordered collapsible>
          <a-list :data-source="systemHealth" bordered>
            <template #renderItem="{ item }">
              <a-list-item>
                <a-space direction="vertical" style="width: 100%;">
                  <div class="health-row">
                    <a-badge :status="statusMap[item.status]?.status" />
                    <span class="health-label">{{ item.label }}</span>
                  </div>
                  <div class="health-message">{{ item.message }}</div>
                </a-space>
              </a-list-item>
            </template>
          </a-list>
        </CardContainer>
      </a-col>
    </a-row>

    <a-row :gutter="16" style="margin-top: 16px;">
      <a-col :span="12">
        <CardContainer title="Recent Activity" bordered collapsible>
          <a-timeline :items="activityTimeline" />
        </CardContainer>
      </a-col>
      <a-col :span="12">
        <CardContainer title="Quick Actions" bordered collapsible>
          <a-space direction="vertical" style="width: 100%;">
            <a-button type="primary" block @click="refresh">Refresh metrics</a-button>
            <a-button block @click="navigate('/users/list')">Create user</a-button>
            <a-button block @click="navigate('/roles/list')">Review roles</a-button>
          </a-space>
        </CardContainer>
      </a-col>
    </a-row>
  </div>
  <Loading v-else overlay tip="Loading dashboard" />
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { message } from "ant-design-vue"
import { dashboardApi } from "../../api/dashboard"
import CardContainer from "../../components/layout/CardContainer.vue"
import Loading from "../../components/common/Loading.vue"

const router = useRouter()

const loading = ref(true)
const summaryCards = ref([])
const chartData = ref([])
const systemHealth = ref([])
const recentActivities = ref([])

const statusMap = {
  operational: { status: "success", label: "Operational" },
  degraded: { status: "warning", label: "Degraded" },
  down: { status: "error", label: "Down" }
}

const chartColumns = [
  { title: "Day", dataIndex: "label", key: "label" },
  { title: "API Requests", dataIndex: "api", key: "api" },
  { title: "Active Users", dataIndex: "users", key: "users" }
]

const chartRows = computed(() =>
  chartData.value.map((row) => ({
    label: row.label,
    api: row.series[0],
    users: row.series[1]
  }))
)

const activityTimeline = computed(() =>
  recentActivities.value.map((item) => ({
    children: `${item.time} – ${item.user} ${item.action} (${item.target})`
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
    message.error("Failed to load dashboard data")
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

onMounted(loadMetrics)
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.metric-value {
  font-size: 28px;
  font-weight: 600;
}

.metric-change {
  margin-top: 4px;
  font-size: 14px;
}

.metric-change.up {
  color: #16a34a;
}

.metric-change.down {
  color: #dc2626;
}

.metric-change.flat {
  color: #6b7280;
}

.health-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.health-label {
  font-weight: 600;
}

.health-message {
  font-size: 12px;
  color: #6b7280;
}
</style>
