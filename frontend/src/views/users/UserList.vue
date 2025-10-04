<template>
  <div class="user-list">
    <SearchForm
      :items="searchItems"
      v-model="formValues"
      @submit="handleSearch"
      @reset="handleReset"
    >
      <template #extra>
        <a-space>
          <a-button type="primary" @click="createUser">New User</a-button>
          <a-button @click="exportUsers">Export</a-button>
        </a-space>
      </template>
    </SearchForm>

    <CardContainer title="User List" bordered :collapsible="false" style="margin-top: 16px;">
      <template #actions>
        <a-space>
          <a-button
            :disabled="selectedRowKeys.length === 0"
            @click="bulkDisable"
          >Disable Selected</a-button>
          <a-button
            danger
            :disabled="selectedRowKeys.length === 0"
            @click="showDeleteDialog = true"
          >Delete Selected</a-button>
        </a-space>
      </template>

      <Table
        :columns="columns"
        :data-source="users"
        :loading="loading"
        :row-selection="rowSelection"
        :pagination="false"
        @change="handleTableChange"
        row-key="id"
      >
        <template #name="{ record }">
          <a-space>
            <UserAvatar :name="record.name" :src="record.avatar" />
            <div>
              <div class="user-name">{{ record.name }}</div>
              <div class="user-email">{{ record.email }}</div>
            </div>
          </a-space>
        </template>
        <template #status="{ record }">
          <StatusTag :status="record.status" />
        </template>
        <template #actions="{ record }">
          <a-space>
            <a-button type="link" size="small" @click="viewUser(record.id)">View</a-button>
            <a-button type="link" size="small" @click="editUser(record.id)">Edit</a-button>
            <a-button type="link" size="small" @click="toggleStatus(record.id)">
              {{ record.status === 'active' ? 'Disable' : 'Enable' }}
            </a-button>
          </a-space>
        </template>
      </Table>

      <div class="table-footer">
        <Pagination
          :total="total"
          v-model:current="pagination.page"
          v-model:page-size="pagination.pageSize"
          @change="handlePageChange"
        />
      </div>
    </CardContainer>

    <ConfirmDialog
      v-model:open="showDeleteDialog"
      title="Delete Users"
      :loading="deleting"
      @confirm="deleteSelected"
      @cancel="() => (showDeleteDialog = false)"
    >
      This action will permanently remove the selected users. Continue?
    </ConfirmDialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue"
import { useRouter } from "vue-router"
import { message } from "ant-design-vue"
import { storeToRefs } from "pinia"
import SearchForm from "../../components/common/SearchForm.vue"
import Table from "../../components/common/Table.vue"
import Pagination from "../../components/common/Pagination.vue"
import CardContainer from "../../components/layout/CardContainer.vue"
import ConfirmDialog from "../../components/common/ConfirmDialog.vue"
import StatusTag from "../../components/business/StatusTag.vue"
import UserAvatar from "../../components/business/UserAvatar.vue"
import { useUserStore } from "../../store/user"

const router = useRouter()
const userStore = useUserStore()

const { list, total, loading, pagination, selectedRowKeys } = storeToRefs(userStore)

const formValues = reactive({ ...userStore.filters })

const searchItems = [
  { key: "keyword", label: "Keyword", component: "a-input", props: { placeholder: "Name or email" } },
  {
    key: "status",
    label: "Status",
    component: "a-select",
    props: {
      options: [
        { label: "All", value: "all" },
        { label: "Active", value: "active" },
        { label: "Inactive", value: "inactive" },
        { label: "Pending", value: "pending" }
      ]
    }
  },
  {
    key: "role",
    label: "Role",
    component: "a-select",
    props: {
      options: [
        { label: "All", value: "all" },
        { label: "Admin", value: "admin" },
        { label: "Manager", value: "manager" },
        { label: "Support", value: "support" },
        { label: "User", value: "user" }
      ]
    }
  },
  {
    key: "department",
    advanced: true,
    label: "Department",
    component: "a-select",
    props: {
      mode: "multiple",
      placeholder: "Departments",
      options: [
        { label: "Operations", value: "Operations" },
        { label: "Engineering", value: "Engineering" },
        { label: "Support", value: "Support" },
        { label: "Finance", value: "Finance" }
      ]
    }
  }
]

const columns = [
  { title: "User", dataIndex: "name", key: "name", slots: { customRender: "name" }, sorter: true },
  { title: "Role", dataIndex: "roleName", key: "roleName" },
  { title: "Department", dataIndex: "department", key: "department" },
  { title: "Status", dataIndex: "status", key: "status", slots: { customRender: "status" } },
  { title: "Last Login", dataIndex: "lastLogin", key: "lastLogin", sorter: true },
  { title: "Actions", key: "actions", slots: { customRender: "actions" }, width: 220 }
]

const users = computed(() => list.value)

const rowSelection = computed(() => ({
  selectedRowKeys: selectedRowKeys.value,
  onChange: (keys) => userStore.setSelectedRowKeys(keys)
}))

const showDeleteDialog = ref(false)
const deleting = ref(false)

const handleSearch = () => {
  userStore.setFilters({ ...formValues })
  userStore.setPagination({ page: 1 })
  userStore.fetchUsers()
}

const handleReset = () => {
  Object.assign(formValues, {
    keyword: "",
    status: "all",
    role: "all",
    department: []
  })
  userStore.resetFilters()
  userStore.setPagination({ page: 1 })
  userStore.fetchUsers()
}

const handlePageChange = ({ page, pageSize }) => {
  userStore.setPagination({ page, pageSize })
  userStore.fetchUsers()
}

const handleTableChange = (paginationConfig, filters, sorter) => {
  const { order, field } = sorter
  userStore.setSorter(order ? { field, order } : null)
  userStore.fetchUsers()
}

const viewUser = (id) => {
  router.push(`/users/${id}`)
}

const editUser = (id) => {
  router.push(`/users/${id}/edit`)
}

const toggleStatus = async (id) => {
  try {
    await userStore.toggleUserStatus(id)
    message.success("User status updated")
  } catch (error) {
    message.error("Failed to update user status")
  }
}

const bulkDisable = async () => {
  try {
    await Promise.all(selectedRowKeys.value.map((id) => userStore.toggleUserStatus(id)))
    message.success("Selected users toggled")
  } catch (error) {
    message.error("Bulk operation failed")
  }
}

const createUser = () => {
  router.push('/users/create')
}

const exportUsers = () => {
  message.info("Exporting mock data")
}

const deleteSelected = async () => {
  deleting.value = true
  try {
    await userStore.deleteUsers(selectedRowKeys.value)
    message.success("Users deleted")
    showDeleteDialog.value = false
  } catch (error) {
    message.error("Delete failed")
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  userStore.fetchUsers()
})
</script>

<style scoped>
.user-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.table-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.user-name {
  font-weight: 600;
}

.user-email {
  font-size: 12px;
  color: #6b7280;
}
</style>
