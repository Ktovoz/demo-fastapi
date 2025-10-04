<template>
  <AuthLayout>
    <a-card class="auth-card" :bordered="false">
      <a-row class="auth-card__content" :gutter="0">
        <a-col :xs="24" :lg="10" class="auth-card__intro">
          <div class="intro-top">
            <div class="intro-badge">演示环境</div>
            <h2 class="intro-title">欢迎回到 Demo FastAPI 管理后台</h2>
            <p class="intro-text">
              体验基于 FastAPI + Vue3 + Ant Design Vue 构建的现代化管理模板，
              了解从登录到权限控制的完整流程。
            </p>
          </div>
          <ul class="intro-list">
            <li>响应式布局与深浅主题可扩展</li>
            <li>Mock 数据支撑的前后台解耦演示</li>
            <li>Pinia 状态管理与路由守卫示例</li>
          </ul>
          <div class="intro-footer">
            <span class="author-note">作者：ktovoz</span>
            <span class="version-note">版本：演示 v1.0</span>
          </div>
        </a-col>
        <a-col :xs="24" :lg="14" class="auth-card__form">
          <div class="form-header">
            <h3>账户登录</h3>
            <p>使用公司邮箱登录，或一键填充演示管理员账号。</p>
          </div>
          <a-form layout="vertical" @finish="handleSubmit" :model="form" class="form-body">
            <a-form-item label="Email" name="email" :rules="[{ required: true, message: 'Email is required' }]">
              <a-input v-model:value="form.email" placeholder="you@example.com" />
            </a-form-item>
            <a-form-item label="Password" name="password" :rules="[{ required: true, message: 'Password is required' }]">
              <a-input-password v-model:value="form.password" placeholder="Enter password" />
            </a-form-item>
            <div class="form-options">
              <a-checkbox v-model:checked="form.remember">Remember me</a-checkbox>
              <router-link to="/auth/forgot-password">Forgot password?</router-link>
            </div>
            <a-space direction="vertical" size="middle" style="width: 100%;">
              <a-button class="demo-button" block @click="fillDemoAccount">
                使用演示管理员账号
              </a-button>
              <a-button type="primary" html-type="submit" block size="large" :loading="authStore.loading">
                登录系统
              </a-button>
            </a-space>
            <a-divider />
            <div class="form-footer">
              <span>还没有账号？</span>
              <a @click.prevent="goRegister">立即注册</a>
            </div>
          </a-form>
        </a-col>
      </a-row>
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
.auth-card {
  cursor: default;
  max-width: 960px;
  margin: 0 auto;
  border-radius: 24px;
  overflow: hidden;
  backdrop-filter: blur(4px);
  box-shadow: 0 40px 80px rgba(15, 23, 42, 0.18);
}

.auth-card__content {
  min-height: 480px;
  align-items: stretch;
}

.auth-card__intro {
  position: relative;
  background: linear-gradient(200deg, #0ea5e9 0%, #2563eb 55%, #1e3a8a 100%);
  color: #e2e8f0;
  padding: 48px 36px;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.auth-card__intro::after {
  content: '';
  position: absolute;
  inset: 14% 18% auto auto;
  width: 160px;
  height: 160px;
  background: radial-gradient(circle at center, rgba(255, 255, 255, 0.45), transparent 65%);
  opacity: 0.6;
  filter: blur(2px);
}

.intro-top {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.intro-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.18);
  border-radius: 999px;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #f8fafc;
}

.intro-title {
  margin: 0;
  font-size: 28px;
  line-height: 1.35;
  color: #f1f5f9;
}

.intro-text {
  margin: 0;
  font-size: 14px;
  color: rgba(241, 245, 249, 0.9);
}

.intro-list {
  margin: 0;
  padding-left: 18px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
  color: rgba(226, 232, 240, 0.85);
}

.intro-list li::marker {
  color: rgba(148, 203, 255, 0.9);
}

.intro-footer {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: rgba(226, 232, 240, 0.75);
}

.auth-card__form {
  padding: 48px 56px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
}

.form-header h3 {
  margin: 0;
  font-size: 26px;
  font-weight: 600;
  color: #0f172a;
}

.form-header p {
  margin: 6px 0 24px;
  color: #64748b;
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px;
  color: #64748b;
}

.demo-button {
  background: rgba(37, 99, 235, 0.12);
  border: 1px solid rgba(37, 99, 235, 0.35);
  color: #1d4ed8;
  font-weight: 500;
}

.demo-button:hover {
  background: rgba(37, 99, 235, 0.2);
  color: #1d4ed8;
}

.form-footer {
  display: flex;
  justify-content: center;
  gap: 6px;
  color: #64748b;
  font-size: 14px;
}

.form-footer a {
  color: #2563eb;
}

@media (max-width: 1024px) {
  .auth-card__form {
    padding: 40px;
  }
}

@media (max-width: 768px) {
  .auth-card {
    border-radius: 20px;
  }

  .auth-card__intro {
    padding: 32px 28px;
  }

  .auth-card__form {
    padding: 32px 24px 40px;
  }

  .form-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
