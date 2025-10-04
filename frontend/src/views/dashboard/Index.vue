<template>
  <div class="dashboard">
    <a-row :gutter="16">
      <a-col :span="6" v-for="card in summaryCards" :key="card.key">
        <CardContainer :title="card.title" bordered>
          <div class="metric-value">{{ card.value }}</div>
          <div class="metric-sub">{{ card.subtitle }}</div>
        </CardContainer>
      </a-col>
    </a-row>

    <a-row :gutter="16" style="margin-top: 16px;">
      <a-col :span="16">
        <CardContainer title="Recent Activity" bordered>
          <a-empty description="Mock data pending" />
        </CardContainer>
      </a-col>
      <a-col :span="8">
        <CardContainer title="System Status" bordered>
          <ul class="status-list">
            <li v-for="item in systemStatus" :key="item.label">
              <StatusTag :status="item.status" />
              <span class="status-label">{{ item.label }}</span>
            </li>
          </ul>
        </CardContainer>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CardContainer from '../../components/layout/CardContainer.vue'
import StatusTag from '../../components/business/StatusTag.vue'

const summaryCards = ref([
  { key: 'users', title: 'Users', value: 128, subtitle: 'Active this week' },
  { key: 'roles', title: 'Roles', value: 6, subtitle: 'Configured roles' },
  { key: 'requests', title: 'Requests', value: 842, subtitle: 'Total API calls' },
  { key: 'errors', title: 'Errors', value: 4, subtitle: 'Last 24 hours' }
])

const systemStatus = ref([
  { label: 'API Service', status: 'active' },
  { label: 'Scheduler', status: 'pending' },
  { label: 'Email Provider', status: 'active' },
  { label: 'Storage', status: 'active' }
])
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.metric-value {
  font-size: 24px;
  font-weight: 600;
}

.metric-sub {
  color: rgba(0, 0, 0, 0.45);
}

.status-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-label {
  margin-left: 8px;
}
</style>
