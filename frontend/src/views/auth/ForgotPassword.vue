<template>
  <AuthLayout>
    <a-card title="Reset Password">
      <a-form layout="vertical" @finish="handleSubmit" :model="form">
        <a-form-item label="Email" name="email" :rules="[{ required: true, message: 'Email is required' }]"><a-input v-model:value="form.email" placeholder="you@example.com" /></a-form-item>
        <a-button type="primary" html-type="submit" block :loading="loading">Send reset link</a-button>
        <a-button type="link" block @click="goBack">Back to sign in</a-button>
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
const form = reactive({ email: '' })

const handleSubmit = async () => {
  loading.value = true
  try {
    await authApi.requestPasswordReset({ email: form.email })
    message.success('Reset email sent (mock)')
    router.push('/auth/login')
  } catch (error) {
    message.error(error?.message || 'Request failed')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/auth/login')
}
</script>

