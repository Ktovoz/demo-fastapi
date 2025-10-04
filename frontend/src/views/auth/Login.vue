<template>
  <AuthPage
    theme="blue"
    :config="pageConfig"
    :form-model="form"
    :loading="authStore.loading"
    @submit="handleSubmit"
  >
    <!-- 左侧特色内容 -->
    <template #features>
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
    </template>

    <!-- 表单提示信息 -->
    <template #alert>
      <div class="form-demo">
        <ThunderboltOutlined />
        <div class="form-demo__content">
          <strong>快速体验</strong>
          <span>一键填充后点击"登录系统"即可进入仪表盘。</span>
        </div>
        <a-button type="link" size="small" class="form-demo__action" @click="fillDemoAccount">
          填充演示账号
        </a-button>
      </div>
    </template>

    <!-- 表单内容 -->
    <template #form>
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
    </template>

    <!-- 表单操作按钮 -->
    <template #actions="{ loading }">
      <a-button
        type="primary"
        html-type="submit"
        block
        size="large"
        :loading="loading"
      >
        登录系统
      </a-button>

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
    </template>
  </AuthPage>
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
import AuthPage from '../../components/AuthPage.vue'
import { useAuthStore } from '../../store/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: '',
  remember: true
})

// 页面配置
const pageConfig = {
  badge: '官方演示环境',
  title: '欢迎回到 Demo FastAPI 管理控制中心',
  description: '探索由 FastAPI、Vue 3 与 Ant Design Vue 驱动的现代化中台模板，从权限守卫到日志追踪一应俱全。',
  formTitle: '账户登录',
  formDescription: '使用企业邮箱登录，也可以一键填充演示管理员账号，直接体验完整流程。',
  meta: '版本：Demo v1.0',
  support: '自动同步测试账号',
  supportIcon: RobotOutlined
}

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
.intro-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}

.metric-card {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 12px 14px;
  border-radius: 12px;
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid rgba(148, 163, 184, 0.2);
  backdrop-filter: blur(8px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.metric-card:hover::before {
  opacity: 1;
}

.metric-card:hover {
  background: rgba(15, 23, 42, 0.5);
  border-color: rgba(59, 130, 246, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
}

.metric-card strong {
  font-size: 18px;
  color: #f8fafc;
  letter-spacing: 0.01em;
  font-weight: 600;
  line-height: 1.2;
}

.metric-card span {
  font-size: 11px;
  color: rgba(226, 232, 240, 0.8);
  font-weight: 400;
  line-height: 1.3;
}

.intro-list {
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  list-style: none;
  margin-bottom: 8px;
}

.intro-list li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 13px;
  color: rgba(226, 232, 240, 0.9);
  line-height: 1.4;
  transition: all 0.2s ease;
  letter-spacing: 0.01em;
}

.intro-list li:hover {
  color: #f8fafc;
  transform: translateX(3px);
}

.list-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 6px;
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
  margin-top: 1px;
}

.intro-list li:hover .list-icon {
  background: rgba(59, 130, 246, 0.25);
  color: #93c5fd;
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.list-icon .anticon {
  font-size: 10px;
}

.form-demo {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 12px;
  align-items: center;
  padding: 14px 16px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(219, 234, 254, 0.8), rgba(191, 219, 254, 0.9));
  border: 1px solid rgba(59, 130, 246, 0.2);
  color: #1e293b;
  backdrop-filter: blur(8px);
  transition: all 0.3s ease;
  margin-bottom: 4px;
}

.form-demo:hover {
  background: linear-gradient(135deg, rgba(219, 234, 254, 0.9), rgba(191, 219, 254, 1));
  border-color: rgba(59, 130, 246, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1);
}

.form-demo .anticon {
  color: #3b82f6;
  font-size: 15px;
}

.form-demo__content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 13px;
  color: #475569;
}

.form-demo__content strong {
  font-size: 13px;
  color: #1d4ed8;
  font-weight: 600;
}

.form-demo__action {
  font-weight: 500;
  color: #1d4ed8 !important;
  transition: all 0.2s ease;
  font-size: 12px;
}

.form-demo__action:hover {
  color: #1e40af !important;
  transform: translateY(-1px);
}

.input-icon {
  color: #94a3b8;
  transition: color 0.2s ease;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #64748b;
  font-size: 14px;
  margin-top: 2px;
}

.form-options a {
  color: #3b82f6;
  font-weight: 500;
  transition: all 0.2s ease;
}

.form-options a:hover {
  color: #2563eb;
  transform: translateY(-1px);
}

.form-divider {
  margin: 16px 0 12px;
}

.form-divider :deep(.ant-divider) {
  color: #94a3b8;
  font-size: 13px;
  margin: 0;
}

.form-social {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  width: 100%;
  margin-bottom: 16px;
}

.form-social .ant-btn {
  height: 44px;
  font-weight: 500;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  color: #475569;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.form-social .ant-btn:hover {
  border-color: #cbd5e1;
  background: #f8fafc;
  color: #334155;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.form-social .ant-btn .anticon {
  color: #64748b;
  transition: color 0.2s ease;
}

.form-social .ant-btn:hover .anticon {
  color: #3b82f6;
}

.form-footer {
  display: flex;
  justify-content: center;
  gap: 8px;
  color: #64748b;
  font-size: 14px;
  margin-top: 12px;
}

.form-footer a {
  color: #3b82f6;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.form-footer a:hover {
  color: #2563eb;
  transform: translateY(-1px);
}

/* 表单输入框样式优化 */
:deep(.ant-form-item-label > label) {
  color: #374151;
  font-weight: 500;
  font-size: 14px;
}

:deep(.ant-input),
:deep(.ant-input-password) {
  border-radius: 10px;
  border: 1px solid #d1d5db;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 15px;
  padding: 12px 16px;
}

:deep(.ant-input:hover),
:deep(.ant-input-password:hover) {
  border-color: #9ca3af;
  background-color: #fafafa;
}

:deep(.ant-input:focus),
:deep(.ant-input-focused),
:deep(.ant-input-password:focus),
:deep(.ant-input-password-focused) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  background-color: #ffffff;
}

:deep(.ant-input-affix-wrapper) {
  border-radius: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.ant-input-affix-wrapper:hover) {
  border-color: #9ca3af;
}

:deep(.ant-input-affix-wrapper-focused) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

:deep(.ant-input-password .ant-input) {
  border: none;
  box-shadow: none;
  padding: 0;
}

:deep(.ant-input-password .ant-input:hover) {
  border: none;
  box-shadow: none;
  background-color: transparent;
}

:deep(.ant-input-password .ant-input:focus) {
  border: none;
  box-shadow: none;
  background-color: transparent;
}

/* 主要按钮样式优化 */
:deep(.ant-btn-primary) {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border: none;
  border-radius: 10px;
  height: 48px;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

:deep(.ant-btn-primary:hover) {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
}

:deep(.ant-btn-primary:active) {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

:deep(.ant-btn-loading) {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}

/* 复选框样式优化 */
:deep(.ant-checkbox) {
  margin-right: 6px;
}

:deep(.ant-checkbox-wrapper) {
  color: #64748b;
  font-size: 14px;
  transition: color 0.2s ease;
}

:deep(.ant-checkbox-wrapper:hover) {
  color: #374151;
}

:deep(.ant-checkbox-inner) {
  border-radius: 6px;
  border-color: #d1d5db;
  transition: all 0.2s ease;
}

:deep(.ant-checkbox-wrapper:hover .ant-checkbox-inner) {
  border-color: #9ca3af;
}

:deep(.ant-checkbox-checked .ant-checkbox-inner) {
  background-color: #3b82f6;
  border-color: #3b82f6;
}

:deep(.ant-checkbox-checked::after) {
  border-color: #ffffff;
}

/* 表单布局优化 */
:deep(.ant-form-item) {
  margin-bottom: 16px;
}

:deep(.ant-form-item:last-child) {
  margin-bottom: 0;
}

:deep(.ant-form-item-explain-error) {
  font-size: 12px;
  color: #ef4444;
  margin-top: 6px;
}

/* 加载状态优化 */
:deep(.ant-btn-loading-icon) {
  color: #ffffff;
}

/* 响应式优化 */
@media (max-width: 992px) {
  .intro-metrics {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
    margin-bottom: 20px;
  }

  .metric-card {
    padding: 10px 12px;
    gap: 1px;
  }

  .metric-card strong {
    font-size: 16px;
  }

  .metric-card span {
    font-size: 10px;
  }

  .intro-list {
    gap: 8px;
  }

  .intro-list li {
    font-size: 12px;
    gap: 8px;
    line-height: 1.3;
  }

  .list-icon {
    width: 16px;
    height: 16px;
    margin-top: 0;
  }

  .list-icon .anticon {
    font-size: 9px;
  }
}

@media (max-width: 576px) {
  .intro-metrics {
    grid-template-columns: repeat(1, minmax(0, 1fr));
    gap: 8px;
    margin-bottom: 16px;
  }

  .metric-card {
    padding: 10px 12px;
    gap: 1px;
  }

  .metric-card strong {
    font-size: 15px;
  }

  .metric-card span {
    font-size: 10px;
  }

  .form-social {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }

  .form-demo {
    grid-template-columns: auto 1fr;
    gap: 8px;
    padding: 12px 14px;
  }

  .form-demo__action {
    grid-column: span 2;
    justify-self: end;
  }

  .intro-list {
    gap: 7px;
  }

  .intro-list li {
    font-size: 11px;
    gap: 7px;
    line-height: 1.3;
  }

  .list-icon {
    width: 15px;
    height: 15px;
    margin-top: 0;
  }

  .list-icon .anticon {
    font-size: 8px;
  }

  .form-options {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .form-footer {
    font-size: 12px;
  }
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.intro-metrics,
.intro-list {
  animation: fadeInUp 0.6s ease-out;
}

.intro-list {
  animation-delay: 0.2s;
}

.form-demo {
  animation: fadeInUp 0.6s ease-out;
  animation-delay: 0.4s;
}
</style>