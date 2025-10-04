<template>
  <CardContainer title="Roles" bordered>
    <Table :columns="columns" :data-source="roles" :loading="loading" row-key="id">
      <template #permissions="{ record }">
        <a-space wrap>
          <a-tag v-for="permission in record.permissions" :key="permission">{{ permission }}</a-tag>
        </a-space>
      </template>
      <template #status="{ record }">
        <StatusTag :status="record.status" />
      </template>
      <template #actions="{ record }">
        <a-space>
          <a-button type="link" size="small" @click="editRole(record.id)">Edit</a-button>
        </a-space>
      </template>
    </Table>
  </CardContainer>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import CardContainer from '../../components/layout/CardContainer.vue'
import Table from '../../components/common/Table.vue'
import StatusTag from '../../components/business/StatusTag.vue'
import { useRoleStore } from '../../store/role'

const router = useRouter()
const roleStore = useRoleStore()
const { list, loading } = storeToRefs(roleStore)

const roles = computed(() => list.value)

const columns = [
  { title: 'Role', dataIndex: 'displayName', key: 'displayName' },
  { title: 'Description', dataIndex: 'description', key: 'description' },
  { title: 'Members', dataIndex: 'members', key: 'members', width: 120 },
  { title: 'Permissions', key: 'permissions', slots: { customRender: 'permissions' } },
  { title: 'Status', key: 'status', slots: { customRender: 'status' }, width: 140 },
  { title: 'Actions', key: 'actions', slots: { customRender: 'actions' }, width: 120 }
]

const editRole = (id) => {
  router.push(`/roles/${id}/edit`)
}

onMounted(() => {
  roleStore.fetchRoles()
})
</script>

