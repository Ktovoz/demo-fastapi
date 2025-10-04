<template>
  <AuthLayout>
    <a-card class="auth-card" :bordered="false">
      <a-row class="auth-card__content" :gutter="0">
        <a-col :xs="24" :lg="10" class="auth-card__intro">
          <div class="intro-pattern intro-pattern--one"></div>
          <div class="intro-pattern intro-pattern--two"></div>
          <div class="intro-top">
            <div class="intro-badge">
              <span class="badge-dot"></span>
              官方演示环境
            </div>
            <h2 class="intro-title">欢迎回到 Demo FastAPI 管理控制中心</h2>
            <p class="intro-text">
              探索由 FastAPI、Vue 3 与 Ant Design Vue 驱动的现代化中台模板，从权限守卫到日志追踪一应俱全。
            </p>
          </div>
          <div class="intro-metrics">
            <div class="metric-card">
              <strong>12+</strong>
              <span>预置模块场景</span>
            </div>
            <div class="metric-card">
              <strong>秒级</strong>
              <span>本地启动体验</span>
            </div>
            <div class="metric-card">
              <strong>24/7</strong>
              <span>持续同步主干</span>
            </div>
          </div>
          <ul class="intro-list">
            <li>
              <span class="list-icon">
                <CheckOutlined />
              </span>
              深浅主题、响应式布局随手切换
            </li>
            <li>
              <span class="list-icon">
                <CheckOutlined />
              </span>
              Pinia 状态与路由守卫全链路示例
            </li>
            <li>
              <span class="list-icon">
                <CheckOutlined />
              </span>
              Mock 数据驱动的前后端解耦
            </li>
          </ul>
          <div class="intro-footer">
            <div class="intro-author">
              <span>作者：ktovoz</span>
              <span class="divider">|</span>
              <span>版本：Demo v1.0</span>
            </div>
            <span class="intro-support">
              <RobotOutlined />
              自动同步测试账号
            </span>
          </div>
        </a-col>
        <a-col :xs="24" :lg="14" class="auth-card__form">
          <div class="form-panel">
            <div class="form-header">
              <h3>账户登录</h3>
              <p>使用企业邮箱登录，也可以一键填充演示管理员账号，直接体验完整流程。</p>
            </div>
            <div class="form-demo">
              <ThunderboltOutlined />
              <div class="form-demo__content">
                <strong>快速体验</strong>
                <span>一键填充后点击“登录系统”即可进入仪表盘。</span>
              </div>
              <a-button type="link" size="small" class="form-demo__action" @click="fillDemoAccount">
                填充演示账号
              </a-button>
            </div>
            <a-form
              layout="vertical"
              @finish="handleSubmit"
              :model="form"
              class="form-body"
            >
              <a-form-item
                label="Email"
                name="email"
                :rules="[{ required: true, message: 'Email is required' }]"
              >
                <a-input
                  v-model:value="form.email"
                  size="large"
                  placeholder="name@company.com"
                  autocomplete="email"
                >
                  <template #prefix>
                    <MailOutlined class="input-icon" />
                  </template>
                </a-input>
              </a-form-item>
              <a-form-item
                label="Password"
                name="password"
                :rules="[{ required: true, message: 'Password is required' }]"
              >
                <a-input-password
                  v-model:value="form.password"
                  size="large"
                  placeholder="输入登录密码"
                  autocomplete="current-password"
                >
                  <template #prefix>
                    <LockOutlined class="input-icon" />
                  </template>
                </a-input-password>
              </a-form-item>
              <div class="form-options">
                <a-checkbox v-model:checked="form.remember">记住我</a-checkbox>
                <router-link to="/auth/forgot-password">忘记密码？</router-link>
              </div>
              <a-button
                type="primary"
                html-type="submit"
                block
                size="large"
                :loading="authStore.loading"
              >
                登录系统
              </a-button>
            </a-form>
            <div class="form-divider">
              <a-divider plain>或使用其他方式登录</a-divider>
            </div>
            <div class="form-social">
              <a-button block @click="handleSocialLogin('github')">
                <template #icon>
                  <GithubOutlined />
                </template>
                GitHub
              </a-button>
              <a-button block @click="handleSocialLogin('google')">
                <template #icon>
                  <GoogleOutlined />
                </template>
                Google
              </a-button>
            </div>
            <div class="form-footer">
              <span>还没有账号？</span>
              <a @click.prevent="goRegister">立即注册</a>
            </div>
          </div>
        </a-col>
      </a-row>
    </a-card>
  </AuthLayout>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import {
  MailOutlined,
  LockOutlined,
  ThunderboltOutlined,
  GithubOutlined,
  GoogleOutlined,
  CheckOutlined,
  RobotOutlined
} from '@ant-design/icons-vue'
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

const handleSocialLogin = (provider) => {
  message.info(`${provider.toUpperCase()} 登录为演示占位，敬请期待`)
}
</script>

<style scoped>
.auth-card {
  position: relative;
  cursor: default;
  max-width: 1024px;
  margin: 0 auto;
  border-radius: 28px;
  overflow: hidden;
  backdrop-filter: blur(6px);
  box-shadow: 0 42px 88px rgba(15, 23, 42, 0.22);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(148, 163, 184, 0.12));
}

.auth-card__content {
  min-height: 520px;
  align-items: stretch;
}

.auth-card__intro {
  position: relative;
  background: radial-gradient(circle at 20% 16%, rgba(56, 189, 248, 0.35), transparent 60%),
    radial-gradient(circle at 80% 75%, rgba(165, 180, 252, 0.25), transparent 58%),
    linear-gradient(210deg, #0f172a 0%, #1e3a8a 48%, #0f172a 100%);
  color: #e2e8f0;
  padding: 52px 42px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  isolation: isolate;
  overflow: hidden;
}

.intro-pattern {
  position: absolute;
  inset: auto;
  border-radius: 100%;
  filter: blur(60px);
  opacity: 0.4;
  pointer-events: none;
  z-index: 0;
}

.intro-pattern--one {
  width: 220px;
  height: 220px;
  background: rgba(14, 165, 233, 0.55);
  top: -80px;
  right: -60px;
}

.intro-pattern--two {
  width: 280px;
  height: 280px;
  background: rgba(94, 234, 212, 0.45);
  bottom: -120px;
  left: -100px;
}

.intro-top,
.intro-metrics,
.intro-list,
.intro-footer {
  position: relative;
  z-index: 1;
}

.intro-top {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.intro-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  background: rgba(15, 23, 42, 0.28);
  border-radius: 999px;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(226, 232, 240, 0.88);
  border: 1px solid rgba(226, 232, 240, 0.25);
}

.badge-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: linear-gradient(135deg, #22d3ee, #38bdf8);
  box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25);
}

.intro-title {
  margin: 0;
  font-size: 30px;
  line-height: 1.35;
  color: #f8fafc;
  font-weight: 600;
}

.intro-text {
  margin: 0;
  font-size: 14px;
  line-height: 1.75;
  color: rgba(226, 232, 240, 0.88);
}

.intro-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.metric-card {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px 18px;
  border-radius: 16px;
  background: rgba(15, 23, 42, 0.35);
  border: 1px solid rgba(148, 163, 184, 0.25);
  backdrop-filter: blur(6px);
}

.metric-card strong {
  font-size: 20px;
  color: #f8fafc;
  letter-spacing: 0.02em;
}

.metric-card span {
  font-size: 12px;
  color: rgba(226, 232, 240, 0.7);
}

.intro-list {
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
  list-style: none;
}

.intro-list li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 13px;
  color: rgba(226, 232, 240, 0.86);
}

.list-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 6px;
  background: rgba(56, 189, 248, 0.18);
  color: #bae6fd;
}

.list-icon .anticon {
  font-size: 12px;
}

.intro-footer {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: rgba(226, 232, 240, 0.78);
}

.intro-author {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.intro-author .divider {
  opacity: 0.6;
}

.intro-support {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.intro-support .anticon {
  color: #bfdbfe;
}

.auth-card__form {
  position: relative;
  padding: 52px 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.94) 0%, rgba(248, 250, 252, 0.9) 100%);
}

.form-panel {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-header h3 {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  color: #0f172a;
}

.form-header p {
  margin: 6px 0 0;
  color: #64748b;
  line-height: 1.6;
}

.form-demo {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 14px;
  align-items: center;
  padding: 14px 16px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(226, 232, 240, 0.6), rgba(191, 219, 254, 0.75));
  border: 1px solid rgba(37, 99, 235, 0.18);
  color: #0f172a;
}

.form-demo__content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 13px;
  color: #334155;
}

.form-demo__content strong {
  font-size: 14px;
  color: #1d4ed8;
}

.form-demo__action {
  font-weight: 500;
  color: #1d4ed8 !important;
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-icon {
  color: #94a3b8;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #64748b;
  font-size: 13px;
}

.form-options a {
  color: #2563eb;
}

.form-divider {
  margin-top: 4px;
}

.form-social {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  width: 100%;
}

.form-social .ant-btn {
  height: 44px;
  font-weight: 500;
}

.form-footer {
  display: flex;
  justify-content: center;
  gap: 8px;
  color: #64748b;
  font-size: 14px;
}

.form-footer a {
  color: #1d4ed8;
  font-weight: 500;
}

@media (max-width: 1200px) {
  .auth-card {
    border-radius: 24px;
  }

  .auth-card__intro {
    padding: 44px 36px;
  }

  .auth-card__form {
    padding: 44px 40px;
  }
}

@media (max-width: 992px) {
  .auth-card__form {
    padding: 38px 28px 44px;
  }

  .intro-metrics {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .auth-card {
    border-radius: 22px;
  }

  .auth-card__intro {
    padding: 32px 26px;
  }

  .auth-card__form {
    padding: 32px 24px 40px;
  }

  .intro-metrics {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 576px) {
  .intro-metrics {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }

  .form-social {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }

  .form-demo {
    grid-template-columns: auto 1fr;
    gap: 10px;
  }

  .form-demo__action {
    grid-column: span 2;
    justify-self: end;
  }
}
</style>