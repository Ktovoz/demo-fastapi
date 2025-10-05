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
          <a-button type="primary" @click="createUser">新建用户</a-button>
          <a-button @click="exportUsers">导出</a-button>
        </a-space>
      </template>
    </SearchForm>

    <CardContainer title="用户列表" bordered :collapsible="false" style="margin-top: 16px;">
      <template #actions>
        <a-space>
          <a-button
            :disabled="selectedRowKeys.length === 0"
            @click="bulkDisable"
          >禁用选中</a-button>
          <a-button
            danger
            :disabled="selectedRowKeys.length === 0"
            @click="showDeleteDialog = true"
          >删除选中</a-button>
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
            <a-button type="link" size="small" @click="viewUser(record.id)">查看</a-button>
            <a-button type="link" size="small" @click="editUser(record.id)">编辑</a-button>
            <a-button type="link" size="small" @click="toggleStatus(record.id)">
              {{ record.status === 'active' ? '禁用' : '启用' }}
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
      title="删除用户"
      :loading="deleting"
      @confirm="deleteSelected"
      @cancel="() => (showDeleteDialog = false)"
    >
      此操作将永久删除选中的用户，是否继续？
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
  { key: "keyword", label: "关键词", component: "a-input", props: { placeholder: "姓名或邮箱" } },
  {
    key: "status",
    label: "状态",
    component: "a-select",
    props: {
      options: [
        { label: "全部", value: "all" },
        { label: "活跃", value: "active" },
        { label: "禁用", value: "inactive" },
        { label: "待审核", value: "pending" }
      ]
    }
  },
  {
    key: "role",
    label: "角色",
    component: "a-select",
    props: {
      options: [
        { label: "全部", value: "all" },
        { label: "管理员", value: "admin" },
        { label: "经理", value: "manager" },
        { label: "客服", value: "support" },
        { label: "普通用户", value: "user" }
      ]
    }
  },
  {
    key: "department",
    advanced: true,
    label: "部门",
    component: "a-select",
    props: {
      mode: "multiple",
      placeholder: "选择部门",
      options: [
        { label: "运营部", value: "Operations" },
        { label: "工程部", value: "Engineering" },
        { label: "客服部", value: "Support" },
        { label: "财务部", value: "Finance" }
      ]
    }
  }
]

const columns = [
  { title: "用户", dataIndex: "name", key: "name", slots: { customRender: "name" }, sorter: true },
  { title: "角色", dataIndex: "roleName", key: "roleName" },
  { title: "部门", dataIndex: "department", key: "department" },
  { title: "状态", dataIndex: "status", key: "status", slots: { customRender: "status" } },
  { title: "最后登录", dataIndex: "lastLogin", key: "lastLogin", sorter: true },
  { title: "操作", key: "actions", slots: { customRender: "actions" }, width: 220 }
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
    message.success("用户状态已更新")
  } catch (error) {
    message.error("更新用户状态失败")
  }
}

const bulkDisable = async () => {
  try {
    await Promise.all(selectedRowKeys.value.map((id) => userStore.toggleUserStatus(id)))
    message.success("选中用户状态已切换")
  } catch (error) {
    message.error("批量操作失败")
  }
}

const createUser = () => {
  router.push('/users/create')
}

const exportUsers = () => {
  message.info("正在导出模拟数据")
}

const deleteSelected = async () => {
  deleting.value = true
  try {
    await userStore.deleteUsers(selectedRowKeys.value)
    message.success("用户已删除")
    showDeleteDialog.value = false
  } catch (error) {
    message.error("删除失败")
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
