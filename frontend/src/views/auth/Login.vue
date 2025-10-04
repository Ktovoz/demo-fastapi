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
      <div class="intro-steps">
        <div class="step-item">
          <span class="step-icon">
            <UserOutlined />
          </span>
          <div class="step-content">
            <strong>快速身份验证</strong>
            <span>支持企业邮箱登录，兼容多租户环境</span>
          </div>
        </div>
        <div class="step-item">
          <span class="step-icon">
            <SafetyOutlined />
          </span>
          <div class="step-content">
            <strong>统一权限管理</strong>
            <span>基于角色的访问控制，精细化权限分配</span>
          </div>
        </div>
        <div class="step-item">
          <span class="step-icon">
            <DashboardOutlined />
          </span>
          <div class="step-content">
            <strong>完整功能体验</strong>
            <span>登录后即可访问完整的仪表盘和系统功能</span>
          </div>
        </div>
      </div>
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
      <div class="form-field-group">
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
            class="form-input"
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
            class="form-input"
          >
            <template #prefix>
              <LockOutlined class="input-icon" />
            </template>
          </a-input-password>
        </a-form-item>
      </div>

      <div class="form-options">
        <a-checkbox v-model:checked="form.remember" class="checkbox-custom">
          <span class="checkbox-label">记住我</span>
        </a-checkbox>
        <router-link to="/auth/forgot-password" class="forgot-link">
          <span class="link-text">忘记密码？</span>
        </router-link>
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
        class="submit-btn"
      >
        <template #loading>
          <LoadingOutlined spin />
        </template>
        <span class="btn-text">登录系统</span>
      </a-button>

      <div class="form-divider">
        <a-divider plain>或使用其他方式登录</a-divider>
      </div>

      <div class="form-social">
        <a-button block @click="handleSocialLogin('github')" class="social-btn">
          <template #icon>
            <GithubOutlined />
          </template>
          <span class="btn-text">GitHub</span>
        </a-button>
        <a-button block @click="handleSocialLogin('google')" class="social-btn">
          <template #icon>
            <GoogleOutlined />
          </template>
          <span class="btn-text">Google</span>
        </a-button>
      </div>

      <div class="form-footer">
        <span class="footer-text">还没有账号？</span>
        <a @click.prevent="goRegister" class="register-link">
          <span class="link-text">立即注册</span>
        </a>
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
  RobotOutlined,
  LoadingOutlined,
  UserOutlined,
  SafetyOutlined,
  DashboardOutlined
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
.intro-steps {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 16px;
  border-radius: 16px;
  background: rgba(30, 58, 138, 0.35);
  border: 1px solid rgba(96, 165, 250, 0.25);
  backdrop-filter: blur(4px);
  transition: all 0.3s ease;
}

.step-item:hover {
  background: rgba(30, 58, 138, 0.45);
  border-color: rgba(96, 165, 250, 0.35);
  transform: translateY(-2px);
}

.step-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(59, 130, 246, 0.25);
  color: #93c5fd;
  font-size: 18px;
  transition: all 0.3s ease;
}

.step-item:hover .step-icon {
  background: rgba(59, 130, 246, 0.35);
  transform: scale(1.05);
}

.step-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.step-content strong {
  font-size: 15px;
  color: #f8fafc;
}

.step-content span {
  font-size: 13px;
  color: rgba(224, 231, 255, 0.78);
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

  .form-field-group {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #64748b;
    font-size: 14px;
    margin-top: 8px;
  }

  .checkbox-custom {
    margin-right: 0;
  }

  .checkbox-label {
    font-size: 13px;
    color: #64748b;
    transition: color 0.2s ease;
  }

  .forgot-link {
    color: #3b82f6;
    font-weight: 500;
    text-decoration: none;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
  }

  .forgot-link::before {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 1px;
    background: linear-gradient(90deg, #3b82f6, #2563eb);
    transition: width 0.3s ease;
  }

  .forgot-link:hover {
    color: #2563eb;
    transform: translateY(-1px);
  }

  .forgot-link:hover::before {
    width: 100%;
  }

  .link-text {
    font-size: 13px;
    font-weight: 500;
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
    align-items: center;
    gap: 8px;
    color: #64748b;
    font-size: 14px;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid rgba(226, 232, 240, 0.6);
  }

  .footer-text {
    font-size: 13px;
    color: #64748b;
  }

  .register-link {
    color: #3b82f6;
    font-weight: 500;
    text-decoration: none;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }

  .register-link::before {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 1px;
    background: linear-gradient(90deg, #3b82f6, #2563eb);
    transition: width 0.3s ease;
  }

  .register-link:hover {
    color: #2563eb;
    transform: translateY(-1px);
  }

  .register-link:hover::before {
    width: 100%;
  }

  .register-link .link-text {
    font-size: 13px;
    font-weight: 500;
  }

/* 表单输入框样式优化 */
:deep(.ant-form-item-label > label) {
  color: #1e293b;
  font-weight: 600;
  font-size: 14px;
  letter-spacing: 0.01em;
}

:deep(.ant-input),
:deep(.ant-input-password) {
  border-radius: 12px;
  border: 1.5px solid #e2e8f0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 15px;
  padding: 14px 16px;
  background: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

:deep(.ant-input:hover),
:deep(.ant-input-password:hover) {
  border-color: #cbd5e1;
  background-color: #f8fafc;
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.08);
}

:deep(.ant-input:focus),
:deep(.ant-input-focused),
:deep(.ant-input-password:focus),
:deep(.ant-input-password-focused) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
  background-color: #ffffff;
  transform: translateY(-1px);
}

:deep(.ant-input-affix-wrapper) {
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.ant-input-affix-wrapper:hover) {
  border-color: #cbd5e1;
}

:deep(.ant-input-affix-wrapper-focused) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
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
  align-items: center;
}

:deep(.ant-checkbox-wrapper:hover) {
  color: #374151;
}

:deep(.ant-checkbox-inner) {
  border-radius: 6px;
  border-color: #d1d5db;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  width: 16px;
  height: 16px;
}

:deep(.ant-checkbox-wrapper:hover .ant-checkbox-inner) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

:deep(.ant-checkbox-checked .ant-checkbox-inner) {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-color: #3b82f6;
}

:deep(.ant-checkbox-checked::after) {
  border-color: #ffffff;
}

:deep(.ant-checkbox-checked .ant-checkbox-inner::after) {
  border-color: #ffffff;
  border-width: 2px;
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
  .step-item {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }

  .step-icon {
    align-self: center;
  }

  .form-social {
    grid-template-columns: repeat(2, minmax(0, 1fr));
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
}

@media (max-width: 576px) {
  .step-item {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }

  .step-icon {
    align-self: center;
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

  .form-options {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .form-footer {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }

  .form-social {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }

  .form-divider {
    margin: 12px 0 8px;
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

.intro-steps {
  animation: fadeInUp 0.6s ease-out;
}

.intro-steps .step-item:nth-child(1) {
  animation-delay: 0.1s;
}

.intro-steps .step-item:nth-child(2) {
  animation-delay: 0.2s;
}

.intro-steps .step-item:nth-child(3) {
  animation-delay: 0.3s;
}

.form-demo {
  animation: fadeInUp 0.6s ease-out;
  animation-delay: 0.4s;
}
</style>