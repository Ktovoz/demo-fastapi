<template>
  <AuthLayout>
    <a-card title="Reset Password">
      <a-form layout="vertical" @finish="handleSubmit">
        <a-form-item label="Email" name="email" :rules="[{ required: true, message: 'Email is required' }]">
          <a-input v-model:value="form.email" placeholder="you@example.com" />
        </a-form-item>
        <a-button type="primary" html-type="submit" block :loading="loading">
          Send reset link
        </a-button>
        <a-button type="link" block @click="goBack">Back to sign in</a-button>
      </a-form>
    </a-card>
  </AuthLayout>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthLayout from '../../layouts/AuthLayout.vue'
import { message } from 'ant-design-vue'

const router = useRouter()
const loading = ref(false)
const form = reactive({
  email: ''
})

const handleSubmit = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    message.success('Reset email sent (mock)')
    router.push('/auth/login')
  }, 800)
}

const goBack = () => {
  router.push('/auth/login')
}
</script>
