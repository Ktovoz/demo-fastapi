<template>
  <AuthLayout>
    <a-card title="Sign In">
      <a-form layout="vertical" @finish="handleSubmit" :model="form">
        <a-form-item label="Email" name="email" :rules="[{ required: true, message: 'Email is required' }]"><a-input v-model:value="form.email" placeholder="you@example.com" /></a-form-item>
        <a-form-item label="Password" name="password" :rules="[{ required: true, message: 'Password is required' }]"><a-input-password v-model:value="form.password" placeholder="Enter password" /></a-form-item>
        <a-form-item>
          <a-checkbox v-model:checked="form.remember">Remember me</a-checkbox>
        </a-form-item>
        <div class="form-actions">
          <router-link to="/auth/forgot-password">Forgot password?</router-link>
        </div>
        <a-button block @click="fillDemoAccount" style="margin-bottom: 12px;">
          使用演示管理员账号
        </a-button>
        <a-button type="primary" html-type="submit" block :loading="authStore.loading">Sign In</a-button>
        <a-button type="link" block @click="goRegister">Create an account</a-button>
        <div class="author-note">作者：ktovoz</div>
      </a-form>
    </a-card>
  </AuthLayout>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import AuthLayout from '../../layouts/AuthLayout.vue'
import { useAuthStore } from '../../store/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: '',
  remember: true
})

const handleSubmit = async () => {
  try {
    await authStore.login(form)
    const redirect = route.query.redirect || '/dashboard'
    router.push(String(redirect))
  } catch (error) {
    message.error(error?.message || 'Sign in failed')
  }
}

const fillDemoAccount = () => {
  form.email = 'admin@example.com'
  form.password = 'admin123'
  form.remember = true
  message.success('已填充演示管理员账号')
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
.author-note {
  margin-top: 16px;
  text-align: center;
  color: rgba(0, 0, 0, 0.45);
  font-size: 12px;
}

</style>

