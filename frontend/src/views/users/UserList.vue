<template>
  <div>
    <SearchForm :items="searchItems" v-model="filters" @submit="handleSearch" />

    <CardContainer title="User List" bordered style="margin-top: 16px;">
      <Table :columns="columns" :data-source="users" :loading="loading">
        <template #actions="{ record }">
          <a-space>
            <a-button type="link" size="small" @click="viewUser(record.id)">View</a-button>
            <a-button type="link" size="small" @click="editUser(record.id)">Edit</a-button>
          </a-space>
        </template>
      </Table>
      <div class="table-footer">
        <Pagination
          :total="total"
          :current="pagination.current"
          :page-size="pagination.pageSize"
          @change="handlePageChange"
        />
      </div>
    </CardContainer>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import SearchForm from '../../components/common/SearchForm.vue'
import Table from '../../components/common/Table.vue'
import Pagination from '../../components/common/Pagination.vue'
import CardContainer from '../../components/layout/CardContainer.vue'

const router = useRouter()
const loading = ref(false)
const total = ref(0)
const users = ref([])
const pagination = reactive({ current: 1, pageSize: 10 })
const filters = ref({})

const columns = [
  { title: 'Name', dataIndex: 'name', key: 'name' },
  { title: 'Email', dataIndex: 'email', key: 'email' },
  { title: 'Role', dataIndex: 'role', key: 'role' },
  { title: 'Status', dataIndex: 'status', key: 'status' },
  { title: 'Actions', key: 'actions', slots: { customRender: 'actions' } }
]

const searchItems = [
  { key: 'keyword', label: 'Keyword', component: 'a-input', props: { placeholder: 'Search users' } },
  { key: 'role', label: 'Role', component: 'a-select', props: { options: [
    { label: 'All', value: undefined },
    { label: 'Admin', value: 'admin' },
    { label: 'Manager', value: 'manager' },
    { label: 'User', value: 'user' }
  ] } }
]

const mockUsers = () => {
  loading.value = true
  setTimeout(() => {
    users.value = Array.from({ length: pagination.pageSize }, (_, index) => ({
      id: index + 1 + (pagination.current - 1) * pagination.pageSize,
      name: `User ${index + 1}`,
      email: `user${index + 1}@example.com`,
      role: index % 2 ? 'admin' : 'user',
      status: index % 2 ? 'Active' : 'Inactive'
    }))
    total.value = 50
    loading.value = false
  }, 400)
}

const handleSearch = () => {
  pagination.current = 1
  mockUsers()
}

const handlePageChange = ({ page, pageSize }) => {
  pagination.current = page
  pagination.pageSize = pageSize
  mockUsers()
}

const viewUser = (id) => {
  router.push(`/users/${id}`)
}

const editUser = (id) => {
  router.push(`/users/${id}/edit`)
}

mockUsers()
</script>

<style scoped>
.table-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>
