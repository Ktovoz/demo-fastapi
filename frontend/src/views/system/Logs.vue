<template>
  <CardContainer title="System Logs" bordered>
    <SearchForm
      :items="searchItems"
      v-model="formValues"
      @submit="handleSearch"
      @reset="handleReset"
    >
      <template #extra>
        <a-button @click="exportLogs">Export</a-button>
      </template>
    </SearchForm>
    <Table
      :columns="columns"
      :data-source="logs"
      :loading="logLoading"
      :pagination="false"
      row-key="id"
      @change="handleTableChange"
    >
      <template #message="{ record }">
        <a-typography-text>{{ record.message }}</a-typography-text>
      </template>
    </Table>
    <div class="table-footer">
      <Pagination
        :total="logTotal"
        v-model:current="logPagination.page"
        v-model:page-size="logPagination.pageSize"
        @change="handlePageChange"
      />
    </div>
  </CardContainer>
</template>

<script setup>
import { reactive } from 'vue'
import { storeToRefs } from 'pinia'
import { message } from 'ant-design-vue'
import CardContainer from '../../components/layout/CardContainer.vue'
import SearchForm from '../../components/common/SearchForm.vue'
import Table from '../../components/common/Table.vue'
import Pagination from '../../components/common/Pagination.vue'
import { useSystemStore } from '../../store/system'

const systemStore = useSystemStore()

const { logs, logTotal, logLoading, logPagination } = storeToRefs(systemStore)

const formValues = reactive({
  keyword: systemStore.logFilters.keyword,
  level: systemStore.logFilters.level
})

const searchItems = [
  { key: 'keyword', label: 'Keyword', component: 'a-input', props: { placeholder: 'Message or module' } },
  {
    key: 'level',
    label: 'Level',
    component: 'a-select',
    props: {
      options: [
        { label: 'All', value: 'ALL' },
        { label: 'Info', value: 'INFO' },
        { label: 'Warn', value: 'WARN' },
        { label: 'Error', value: 'ERROR' }
      ]
    }
  }
]

const columns = [
  { title: 'Timestamp', dataIndex: 'time', key: 'time', sorter: true },
  { title: 'Level', dataIndex: 'level', key: 'level' },
  { title: 'Module', dataIndex: 'module', key: 'module' },
  { title: 'Message', dataIndex: 'message', key: 'message', slots: { customRender: 'message' } }
]

const handleSearch = () => {
  systemStore.setLogFilters({ ...formValues })
  systemStore.setLogPagination({ page: 1 })
  systemStore.fetchLogs()
}

const handleReset = () => {
  systemStore.resetLogFilters()
  Object.assign(formValues, { keyword: '', level: 'ALL' })
  systemStore.setLogPagination({ page: 1 })
  systemStore.fetchLogs()
}

const handlePageChange = ({ page, pageSize }) => {
  systemStore.setLogPagination({ page, pageSize })
  systemStore.fetchLogs()
}

const handleTableChange = (pagination, filters, sorter) => {
  const { order, field } = sorter
  systemStore.setLogSorter(order ? { field, order } : null)
  systemStore.fetchLogs()
}

const exportLogs = () => {
  message.success('Export started (mock)')
}

systemStore.fetchLogs()
</script>

<style scoped>
.table-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>

