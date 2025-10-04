<template>
  <CardContainer title="Edit Role" bordered>
    <Loading v-if="loading" overlay tip="Loading role" />
    <template v-else>
      <a-form layout="vertical" @finish="handleSubmit" :model="form">
        <a-form-item label="Role Name" name="displayName" :rules="[{ required: true, message: 'Role name is required' }]"><a-input v-model:value="form.displayName" /></a-form-item>
        <a-form-item label="Description" name="description"><a-textarea v-model:value="form.description" rows="3" /></a-form-item>
        <a-form-item label="Permissions">
          <PermissionTree :tree-data="treeData" v-model:checkedKeys="form.permissions" />
        </a-form-item>
        <a-form-item label="Status">
          <a-radio-group v-model:value="form.status">
            <a-radio value="active">Active</a-radio>
            <a-radio value="pending">Pending</a-radio>
            <a-radio value="inactive">Inactive</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-space>
          <a-button @click="goBack">Cancel</a-button>
          <a-button type="primary" html-type="submit" :loading="saving">Save</a-button>
        </a-space>
      </a-form>
    </template>
  </CardContainer>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import CardContainer from '../../components/layout/CardContainer.vue'
import PermissionTree from '../../components/business/PermissionTree.vue'
import Loading from '../../components/common/Loading.vue'
import { useRoleStore } from '../../store/role'

const route = useRoute()
const router = useRouter()
const roleStore = useRoleStore()

const loading = ref(true)
const saving = ref(false)

const form = reactive({
  displayName: '',
  description: '',
  permissions: [],
  status: 'active'
})

const treeData = [
  {
    title: 'Users',
    key: 'users',
    children: [
      { title: 'View Users', key: 'users:view' },
      { title: 'Edit Users', key: 'users:edit' },
      { title: 'Delete Users', key: 'users:delete' }
    ]
  },
  {
    title: 'Roles',
    key: 'roles',
    children: [
      { title: 'View Roles', key: 'roles:view' },
      { title: 'Edit Roles', key: 'roles:edit' }
    ]
  },
  {
    title: 'System',
    key: 'system',
    children: [
      { title: 'View Logs', key: 'logs:view' },
      { title: 'Manage System', key: 'system:manage' }
    ]
  }
]

const loadRole = async () => {
  try {
    const role = await roleStore.fetchRoleDetail(route.params.id)
    Object.assign(form, {
      displayName: role.displayName,
      description: role.description,
      permissions: role.permissions ?? [],
      status: role.status ?? 'active'
    })
  } catch (error) {
    message.error('Unable to load role')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  saving.value = true
  try {
    await roleStore.updateRole(route.params.id, {
      displayName: form.displayName,
      description: form.description,
      permissions: [...form.permissions],
      status: form.status
    })
    message.success('Role updated')
    router.push('/roles/list')
  } catch (error) {
    message.error('Failed to save role')
  } finally {
    saving.value = false
  }
}

const goBack = () => {
  router.push('/roles/list')
}

onMounted(loadRole)
</script>

