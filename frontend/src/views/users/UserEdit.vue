<template>
  <CardContainer :title="pageTitle" bordered>
    <a-form layout="vertical" @finish="handleSubmit" :model="form" :disabled="loading">
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="Name" name="name" :rules="[{ required: true, message: 'Name is required' }]">
            <a-input v-model:value="form.name" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="Email" name="email" :rules="[{ required: true, message: 'Email is required' }]">
            <a-input v-model:value="form.email" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="Role" name="role">
            <a-select v-model:value="form.role" :options="roleOptions" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="Status" name="status">
            <a-select v-model:value="form.status" :options="statusOptions" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="Department" name="department">
            <a-select v-model:value="form.department" :options="departmentOptions" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="Phone" name="phone">
            <a-input v-model:value="form.phone" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item label="Tags" name="tags">
        <a-select v-model:value="form.tags" mode="tags" placeholder="Add tags" />
      </a-form-item>
      <a-form-item label="Permissions" name="permissions">
        <a-select v-model:value="form.permissions" mode="multiple" :options="permissionOptions" />
      </a-form-item>
      <a-space>
        <a-button @click="goBack">Cancel</a-button>
        <a-button type="primary" html-type="submit" :loading="submitting">Save</a-button>
      </a-space>
    </a-form>
  </CardContainer>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import CardContainer from '../../components/layout/CardContainer.vue'
import { useUserStore } from '../../store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const submitting = ref(false)
const isCreate = computed(() => route.name === 'UserCreate')

const form = reactive({
  name: '',
  email: '',
  role: 'user',
  status: 'active',
  department: 'Operations',
  phone: '',
  tags: [],
  permissions: ['users:view']
})

const roleOptions = [
  { label: 'Admin', value: 'admin' },
  { label: 'Manager', value: 'manager' },
  { label: 'Support', value: 'support' },
  { label: 'User', value: 'user' }
]

const statusOptions = [
  { label: 'Active', value: 'active' },
  { label: 'Inactive', value: 'inactive' },
  { label: 'Pending', value: 'pending' }
]

const departmentOptions = [
  { label: 'Operations', value: 'Operations' },
  { label: 'Engineering', value: 'Engineering' },
  { label: 'Support', value: 'Support' },
  { label: 'Finance', value: 'Finance' }
]

const permissionOptions = [
  { label: 'View Users', value: 'users:view' },
  { label: 'Edit Users', value: 'users:edit' },
  { label: 'Delete Users', value: 'users:delete' },
  { label: 'View Logs', value: 'logs:view' },
  { label: 'Manage System', value: 'system:manage' }
]

const pageTitle = computed(() => (isCreate.value ? 'Create User' : 'Edit User'))

const loadUser = async () => {
  if (isCreate.value) {
    loading.value = false
    return
  }
  try {
    const user = await userStore.fetchUserDetail(route.params.id)
    Object.assign(form, {
      name: user.name,
      email: user.email,
      role: user.role,
      status: user.status,
      department: user.department,
      phone: user.phone,
      tags: user.tags ?? [],
      permissions: user.permissions ?? []
    })
  } catch (error) {
    message.error('Unable to load user')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    const payload = {
      ...form,
      tags: [...(form.tags || [])],
      permissions: [...(form.permissions || [])]
    }
    if (isCreate.value) {
      await userStore.createUser(payload)
      message.success('User created')
    } else {
      await userStore.updateUser(route.params.id, payload)
      message.success('User updated')
    }
    router.push('/users/list')
  } catch (error) {
    message.error('Failed to save user')
  } finally {
    submitting.value = false
  }
}

const goBack = () => {
  router.push('/users/list')
}

onMounted(loadUser)
</script>

