<template>
  <CardContainer title="Roles" bordered>
    <Table :columns="columns" :data-source="roles">
      <template #members="{ record }">
        <a-space wrap>
          <RoleTag v-for="tag in record.permissions" :key="tag" :role="tag">
            {{ tag }}
          </RoleTag>
        </a-space>
      </template>
      <template #actions="{ record }">
        <a-button type="link" size="small" @click="editRole(record.id)">Edit</a-button>
      </template>
    </Table>
  </CardContainer>
</template>

<script setup>
import { useRouter } from 'vue-router'
import Table from '../../components/common/Table.vue'
import CardContainer from '../../components/layout/CardContainer.vue'
import RoleTag from '../../components/business/RoleTag.vue'

const router = useRouter()

const columns = [
  { title: 'Role', dataIndex: 'name', key: 'name' },
  { title: 'Description', dataIndex: 'description', key: 'description' },
  { title: 'Permissions', key: 'permissions', slots: { customRender: 'members' } },
  { title: 'Actions', key: 'actions', slots: { customRender: 'actions' } }
]

const roles = [
  { id: 1, name: 'Admin', description: 'Full access', permissions: ['admin', 'manage'] },
  { id: 2, name: 'Manager', description: 'Manage teams', permissions: ['manage'] },
  { id: 3, name: 'User', description: 'Standard access', permissions: ['user'] }
]

const editRole = (id) => {
  router.push(`/roles/${id}/edit`)
}
</script>
