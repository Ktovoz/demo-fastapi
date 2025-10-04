<template>
  <AuthLayout>
    <a-card title="Sign In">
      <a-form layout="vertical" @finish="handleSubmit">
        <a-form-item label="Email" name="email" :rules="[{ required: true, message: 'Email is required' }]">
          <a-input v-model:value="form.email" placeholder="you@example.com" />
        </a-form-item>
        <a-form-item label="Password" name="password" :rules="[{ required: true, message: 'Password is required' }]">
          <a-input-password v-model:value="form.password" placeholder="••••••••" />
        </a-form-item>
        <div class="form-actions">
          <router-link to="/auth/forgot-password">Forgot password?</router-link>
        </div>
        <a-button type="primary" html-type="submit" block :loading="loading">
          Sign In
        </a-button>
        <a-button type="link" block @click="goRegister">Create an account</a-button>
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
  email: '',
  password: ''
})

const handleSubmit = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    message.success('Signed in (mock)')
    router.push('/dashboard')
  }, 800)
}

const goRegister = () => {
  router.push('/auth/register')
}
</script>

<style scoped>
.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 12px;
}
</style>
