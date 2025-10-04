<template>
  <AuthLayout>
    <a-card title="Create Account">
      <a-form layout="vertical" @finish="handleSubmit" :model="form">
        <a-form-item label="Full Name" name="name" :rules="[{ required: true, message: 'Name is required' }]"><a-input v-model:value="form.name" placeholder="Jane Doe" /></a-form-item>
        <a-form-item label="Email" name="email" :rules="[{ required: true, message: 'Email is required' }]"><a-input v-model:value="form.email" placeholder="you@example.com" /></a-form-item>
        <a-form-item label="Password" name="password" :rules="[{ required: true, message: 'Password is required' }]"><a-input-password v-model:value="form.password" placeholder="Create a password" /></a-form-item>
        <a-form-item label="Confirm Password" name="confirm" :rules="[{ required: true, validator: validateConfirm }]"><a-input-password v-model:value="form.confirm" placeholder="Repeat your password" /></a-form-item>
        <a-button type="primary" html-type="submit" block :loading="loading">Register</a-button>
        <a-button type="link" block @click="goLogin">Already have an account?</a-button>
      </a-form>
    </a-card>
  </AuthLayout>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import AuthLayout from '../../layouts/AuthLayout.vue'
import { authApi } from '../../api/auth'

const router = useRouter()
const loading = ref(false)
const form = reactive({
  name: '',
  email: '',
  password: '',
  confirm: ''
})

const validateConfirm = (_rule, value) => {
  if (!value) {
    return Promise.reject('Confirm your password')
  }
  if (value !== form.password) {
    return Promise.reject('Passwords do not match')
  }
  return Promise.resolve()
}

const handleSubmit = async () => {
  loading.value = true
  try {
    await authApi.register({ name: form.name, email: form.email, password: form.password })
    message.success('Account created (mock)')
    router.push('/auth/login')
  } catch (error) {
    message.error(error?.message || 'Registration failed')
  } finally {
    loading.value = false
  }
}

const goLogin = () => {
  router.push('/auth/login')
}
</script>

