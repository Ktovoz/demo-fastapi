<template>
  <CardContainer title="Edit Role" bordered>
    <a-form layout="vertical" @finish="handleSubmit">
      <a-form-item label="Role Name" name="name" :rules="[{ required: true, message: 'Role name is required' }]">
        <a-input v-model:value="form.name" />
      </a-form-item>
      <a-form-item label="Description" name="description">
        <a-textarea v-model:value="form.description" rows="3" />
      </a-form-item>
      <a-form-item label="Permissions">
        <PermissionTree :tree-data="treeData" v-model:checkedKeys="form.permissions" />
      </a-form-item>
      <a-space>
        <a-button @click="goBack">Cancel</a-button>
        <a-button type="primary" html-type="submit" :loading="loading">Save</a-button>
      </a-space>
    </a-form>
  </CardContainer>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import CardContainer from '../../components/layout/CardContainer.vue'
import PermissionTree from '../../components/business/PermissionTree.vue'

const router = useRouter()
const loading = ref(false)

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
  }
]

const form = reactive({
  name: 'Manager',
  description: 'Manage team resources',
  permissions: ['users:view', 'roles:view']
})

const handleSubmit = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    message.success('Role saved (mock)')
    router.push('/roles/list')
  }, 500)
}

const goBack = () => {
  router.back()
}
</script>
