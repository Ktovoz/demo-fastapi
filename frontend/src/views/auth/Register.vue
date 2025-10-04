<template>
  <AuthLayout>
    <a-card class="auth-card" :bordered="false">
      <a-row class="auth-card__content" :gutter="0">
        <a-col :xs="24" :lg="10" class="auth-card__intro">
          <div class="intro-decor intro-decor--one"></div>
          <div class="intro-decor intro-decor--two"></div>
          <div class="intro-top">
            <div class="intro-badge">
              <span class="badge-dot"></span>
              快速上手
            </div>
            <h2 class="intro-title">创建账号，开启协同治理新旅程</h2>
            <p class="intro-text">
              注册演示环境，体验统一认证、权限控制与配置治理的完整闭环，快速掌握 Demo FastAPI 的最佳实践。
            </p>
          </div>
          <div class="intro-timeline">
            <div class="timeline-item">
              <span class="timeline-index">01</span>
              <div class="timeline-content">
                <strong>填写基础信息</strong>
                <p>支持企业邮箱校验，兼容个人沙箱体验。</p>
              </div>
            </div>
            <div class="timeline-item">
              <span class="timeline-index">02</span>
              <div class="timeline-content">
                <strong>验证演示权限</strong>
                <p>自动分配默认角色，模拟真实审批流程。</p>
              </div>
            </div>
            <div class="timeline-item">
              <span class="timeline-index">03</span>
              <div class="timeline-content">
                <strong>登录控制中心</strong>
                <p>立即访问仪表盘，查看多租户示例数据。</p>
              </div>
            </div>
          </div>
          <div class="intro-footer">
            <div class="intro-note">
              <span>作者：ktovoz</span>
              <span class="divider">|</span>
              <span>推荐使用企业邮箱注册</span>
            </div>
            <a-tag color="pink-inverse">Mock 环境</a-tag>
          </div>
        </a-col>
        <a-col :xs="24" :lg="14" class="auth-card__form">
          <div class="form-panel">
            <div class="form-header">
              <h3>创建新账号</h3>
              <p>完善基础资料，稍后可在个人中心补全部门、角色等信息。</p>
            </div>
            <a-alert
              type="info"
              message="当前为 Mock 接口，便于快速理解注册流程"
              description="提交后会提示注册成功并跳转至登录页，不会保存真实数据。"
              show-icon
              class="form-alert"
            />
            <a-form layout="vertical" @finish="handleSubmit" :model="form" class="form-body">
              <a-row :gutter="16">
                <a-col :span="24" :md="12">
                  <a-form-item
                    label="姓名"
                    name="name"
                    :rules="[{ required: true, message: 'Name is required' }]"
                  >
                    <a-input
                      v-model:value="form.name"
                      size="large"
                      placeholder="王小明 / Jane Doe"
                      autocomplete="name"
                    >
                      <template #prefix>
                        <UserOutlined class="input-icon" />
                      </template>
                    </a-input>
                  </a-form-item>
                </a-col>
                <a-col :span="24" :md="12">
                  <a-form-item
                    label="工作邮箱"
                    name="email"
                    :rules="[{ required: true, message: 'Email is required' }]"
                  >
                    <a-input
                      v-model:value="form.email"
                      size="large"
                      placeholder="you@example.com"
                      autocomplete="email"
                    >
                      <template #prefix>
                        <MailOutlined class="input-icon" />
                      </template>
                    </a-input>
                  </a-form-item>
                </a-col>
              </a-row>
              <a-row :gutter="16">
                <a-col :span="24" :md="12">
                  <a-form-item
                    label="设置密码"
                    name="password"
                    :rules="[{ required: true, message: 'Password is required' }]"
                  >
                    <a-input-password
                      v-model:value="form.password"
                      size="large"
                      placeholder="至少 8 位，包含数字和字母"
                      autocomplete="new-password"
                    >
                      <template #prefix>
                        <LockOutlined class="input-icon" />
                      </template>
                    </a-input-password>
                  </a-form-item>
                </a-col>
                <a-col :span="24" :md="12">
                  <a-form-item
                    label="确认密码"
                    name="confirm"
                    :rules="[{ required: true, validator: validateConfirm }]"
                  >
                    <a-input-password
                      v-model:value="form.confirm"
                      size="large"
                      placeholder="再次输入密码"
                      autocomplete="new-password"
                    >
                      <template #prefix>
                        <SafetyOutlined class="input-icon" />
                      </template>
                    </a-input-password>
                  </a-form-item>
                </a-col>
              </a-row>
              <ul class="form-tips">
                <li>推荐开启两步验证，提升账号安全性。</li>
                <li>注册成功后，可在“系统设置 → 租户管理”创建测试租户。</li>
              </ul>
              <a-form-item class="form-checkbox">
                <a-checkbox checked disabled>同意 Demo FastAPI 演示环境使用条款</a-checkbox>
              </a-form-item>
              <div class="form-actions">
                <a-button
                  type="primary"
                  html-type="submit"
                  block
                  size="large"
                  :loading="loading"
                >
                  完成注册
                </a-button>
                <a-button block size="large" @click="goLogin">返回登录</a-button>
              </div>
            </a-form>
          </div>
        </a-col>
      </a-row>
    </a-card>
  </AuthLayout>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { UserOutlined, MailOutlined, LockOutlined, SafetyOutlined } from '@ant-design/icons-vue'
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
    message.success('账号已创建（演示环境）')
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
  position: relative;
  cursor: default;
  max-width: 1024px;
  margin: 0 auto;
  border-radius: 28px;
  overflow: hidden;
  backdrop-filter: blur(6px);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(248, 113, 166, 0.08));
  box-shadow: 0 42px 88px rgba(190, 24, 93, 0.18);
}

.auth-card__content {
  min-height: 520px;
  align-items: stretch;
}

.auth-card__intro {
  position: relative;
  padding: 54px 44px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  color: #fff1f2;
  background: radial-gradient(circle at 24% 18%, rgba(251, 113, 133, 0.4), transparent 60%),
    radial-gradient(circle at 75% 82%, rgba(244, 114, 182, 0.35), transparent 55%),
    linear-gradient(210deg, #9d174d 0%, #be123c 52%, #831843 100%);
  isolation: isolate;
  overflow: hidden;
}

.intro-decor {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
  opacity: 0.45;
  pointer-events: none;
  z-index: 0;
}

.intro-decor--one {
  width: 240px;
  height: 240px;
  top: -110px;
  right: -80px;
  background: rgba(253, 164, 175, 0.65);
}

.intro-decor--two {
  width: 280px;
  height: 280px;
  bottom: -130px;
  left: -90px;
  background: rgba(244, 114, 182, 0.55);
}

.intro-top,
.intro-timeline,
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
  background: rgba(131, 24, 67, 0.6);
  border-radius: 999px;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  border: 1px solid rgba(255, 228, 230, 0.35);
  color: rgba(255, 241, 242, 0.9);
}

.badge-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f9a8d4, #f472b6);
  box-shadow: 0 0 0 2px rgba(244, 114, 182, 0.25);
}

.intro-title {
  margin: 0;
  font-size: 30px;
  line-height: 1.35;
  color: #fff7fb;
  font-weight: 600;
}

.intro-text {
  margin: 0;
  font-size: 14px;
  line-height: 1.75;
  color: rgba(255, 241, 242, 0.85);
}

.intro-timeline {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.timeline-item {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 14px;
  align-items: start;
  padding: 14px 16px;
  border-radius: 16px;
  background: rgba(131, 24, 67, 0.45);
  border: 1px solid rgba(248, 113, 166, 0.2);
  backdrop-filter: blur(4px);
}

.timeline-index {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  background: rgba(244, 114, 182, 0.35);
  color: #fff7fb;
}

.timeline-content strong {
  display: block;
  font-size: 15px;
  color: #fdf2f8;
  margin-bottom: 4px;
}

.timeline-content p {
  margin: 0;
  font-size: 13px;
  color: rgba(255, 241, 242, 0.78);
}

.intro-footer {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: rgba(255, 241, 242, 0.8);
}

.intro-note {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.intro-note .divider {
  opacity: 0.6;
}

.auth-card__form {
  padding: 54px 62px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.94) 0%, rgba(255, 247, 253, 0.94) 100%);
}

.form-panel {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-header h3 {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  color: #831843;
}

.form-header p {
  margin: 6px 0 0;
  color: #a855f7;
  line-height: 1.6;
}

.form-alert {
  border-radius: 16px;
  background: rgba(255, 240, 246, 0.8);
  border: 1px solid rgba(236, 72, 153, 0.25);
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-icon {
  color: #c084fc;
}

.form-tips {
  margin: 0;
  padding-left: 18px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
  color: #7e22ce;
}

.form-checkbox {
  margin: 0;
}

.form-actions {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

@media (max-width: 1200px) {
  .auth-card {
    border-radius: 24px;
  }

  .auth-card__intro {
    padding: 44px 38px;
  }

  .auth-card__form {
    padding: 42px 40px;
  }
}

@media (max-width: 992px) {
  .auth-card__form {
    padding: 38px 28px 44px;
  }

  .form-actions {
    grid-template-columns: repeat(1, minmax(0, 1fr));
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
}

@media (max-width: 576px) {
  .timeline-item {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .timeline-index {
    width: 28px;
    height: 28px;
  }
}
</style>