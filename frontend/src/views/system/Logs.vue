<template>
  <CardContainer title="System Logs" bordered>
    <SearchForm :items="searchItems" v-model="filters" @submit="handleSearch">
      <template #extra>
        <a-button @click="exportLogs">Export</a-button>
      </template>
    </SearchForm>
    <Table :columns="columns" :data-source="logs" :loading="loading" />
  </CardContainer>
</template>

<script setup>
import { ref } from 'vue'
import SearchForm from '../../components/common/SearchForm.vue'
import Table from '../../components/common/Table.vue'
import CardContainer from '../../components/layout/CardContainer.vue'

const loading = ref(false)
const filters = ref({})

const searchItems = [
  { key: 'keyword', label: 'Keyword', component: 'a-input', props: { placeholder: 'Search logs' } },
  { key: 'level', label: 'Level', component: 'a-select', props: { options: [
    { label: 'All', value: undefined },
    { label: 'Info', value: 'INFO' },
    { label: 'Warning', value: 'WARN' },
    { label: 'Error', value: 'ERROR' }
  ] } }
]

const columns = [
  { title: 'Timestamp', dataIndex: 'time', key: 'time' },
  { title: 'Level', dataIndex: 'level', key: 'level' },
  { title: 'Message', dataIndex: 'message', key: 'message' },
  { title: 'Module', dataIndex: 'module', key: 'module' }
]

const logs = ref([
  { key: 1, time: '2025-10-04 10:00', level: 'INFO', message: 'System boot', module: 'core' },
  { key: 2, time: '2025-10-04 10:05', level: 'WARN', message: 'High memory usage', module: 'monitor' },
  { key: 3, time: '2025-10-04 10:10', level: 'ERROR', message: 'Job failed', module: 'scheduler' }
])

const handleSearch = () => {}
const exportLogs = () => {}
</script>
