<template>
  <CardContainer title="Edit User" bordered>
    <a-form layout="vertical" @finish="handleSubmit">
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
      <a-space>
        <a-button @click="goBack">Cancel</a-button>
        <a-button type="primary" html-type="submit" :loading="loading">Save</a-button>
      </a-space>
    </a-form>
  </CardContainer>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import CardContainer from '../../components/layout/CardContainer.vue'

const router = useRouter()
const route = useRoute()
const loading = ref(false)

const roleOptions = [
  { label: 'Admin', value: 'admin' },
  { label: 'Manager', value: 'manager' },
  { label: 'User', value: 'user' }
]

const statusOptions = [
  { label: 'Active', value: 'active' },
  { label: 'Inactive', value: 'inactive' }
]

const form = reactive({
  name: 'Mock User',
  email: 'mock@example.com',
  role: 'user',
  status: 'active'
})

const handleSubmit = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    message.success('User updated (mock)')
    router.push(`/users/${route.params.id}`)
  }, 500)
}

const goBack = () => {
  router.back()
}
</script>
