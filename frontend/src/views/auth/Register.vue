<template>
  <AuthLayout>
    <a-card class="auth-card" :bordered="false">
      <a-row class="auth-card__content" :gutter="0">
        <a-col :xs="24" :lg="10" class="auth-card__intro">
          <div class="intro-top">
            <div class="intro-badge">快速上手</div>
            <h2 class="intro-title">创建账号，体验协同管理的完整流程</h2>
            <p class="intro-text">
              通过注册演示账号，了解如何在项目中搭建统一的认证、权限和配置管理模块，
              并快速试用 Mock 数据带来的开发效率提升。
            </p>
          </div>
          <ul class="intro-list">
            <li>统一的 UI 设计体系与布局规范</li>
            <li>多场景的表单校验与交互示例</li>
            <li>便捷扩展的路由与状态组织结构</li>
          </ul>
          <div class="intro-footer">
            <span class="author-note">作者：ktovoz</span>
            <span class="version-note">建议使用公司邮箱注册</span>
          </div>
        </a-col>
        <a-col :xs="24" :lg="14" class="auth-card__form">
          <div class="form-header">
            <h3>创建新账号</h3>
            <p>填写基础信息即可完成注册，稍后可在个人中心完善更多资料。</p>
          </div>
          <a-form layout="vertical" @finish="handleSubmit" :model="form" class="form-body">
            <a-row :gutter="16">
              <a-col :span="24" :md="12">
                <a-form-item label="Full Name" name="name" :rules="[{ required: true, message: 'Name is required' }]">
                  <a-input v-model:value="form.name" placeholder="Jane Doe" />
                </a-form-item>
              </a-col>
              <a-col :span="24" :md="12">
                <a-form-item label="Email" name="email" :rules="[{ required: true, message: 'Email is required' }]">
                  <a-input v-model:value="form.email" placeholder="you@example.com" />
                </a-form-item>
              </a-col>
            </a-row>
            <a-row :gutter="16">
              <a-col :span="24" :md="12">
                <a-form-item label="Password" name="password" :rules="[{ required: true, message: 'Password is required' }]">
                  <a-input-password v-model:value="form.password" placeholder="Create a password" />
                </a-form-item>
              </a-col>
              <a-col :span="24" :md="12">
                <a-form-item label="Confirm Password" name="confirm" :rules="[{ required: true, validator: validateConfirm }]">
                  <a-input-password v-model:value="form.confirm" placeholder="Repeat password" />
                </a-form-item>
              </a-col>
            </a-row>
            <a-form-item>
              <a-checkbox checked disabled>同意 Demo FastAPI 演示环境使用条款</a-checkbox>
            </a-form-item>
            <a-space direction="vertical" size="middle" style="width: 100%;">
              <a-button type="primary" html-type="submit" block size="large" :loading="loading">
                完成注册
              </a-button>
              <a-button block @click="goLogin">返回登录</a-button>
            </a-space>
          </a-form>
        </a-col>
      </a-row>
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

<style scoped>
.auth-card {
  cursor: default;
  max-width: 960px;
  margin: 0 auto;
  border-radius: 24px;
  overflow: hidden;
  backdrop-filter: blur(4px);
  box-shadow: 0 40px 80px rgba(157, 23, 77, 0.16);
}

.auth-card__content {
  min-height: 480px;
  align-items: stretch;
}

.auth-card__intro {
  position: relative;
  background: linear-gradient(200deg, #ec4899 0%, #db2777 55%, #be123c 100%);
  color: #fdf2f8;
  padding: 48px 36px;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.auth-card__intro::after {
  content: '';
  position: absolute;
  inset: auto auto 12% 20%;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle at center, rgba(255, 255, 255, 0.35), transparent 65%);
  opacity: 0.7;
  filter: blur(4px);
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
  background: rgba(255, 255, 255, 0.2);
  border-radius: 999px;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #fdf2f8;
}

.intro-title {
  margin: 0;
  font-size: 28px;
  line-height: 1.35;
  color: #fff7fb;
}

.intro-text {
  margin: 0;
  font-size: 14px;
  color: rgba(253, 242, 248, 0.9);
}

.intro-list {
  margin: 0;
  padding-left: 18px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
  color: rgba(252, 231, 243, 0.9);
}

.intro-list li::marker {
  color: rgba(255, 255, 255, 0.8);
}

.intro-footer {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: rgba(253, 242, 248, 0.75);
}

.auth-card__form {
  padding: 48px 56px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: linear-gradient(180deg, #ffffff 0%, #fff7fb 100%);
}

.form-header h3 {
  margin: 0;
  font-size: 26px;
  font-weight: 600;
  color: #7f1d1d;
}

.form-header p {
  margin: 6px 0 24px;
  color: #a855f7;
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
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
}
</style>
