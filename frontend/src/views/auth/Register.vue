<template>
  <AuthPage
    theme="pink"
    :config="pageConfig"
    :form-model="form"
    :loading="loading"
    @submit="handleSubmit"
  >
    <!-- 左侧特色内容 -->
    <template #features>
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
    </template>

    <!-- 表单提示信息 -->
    <template #alert>
      <a-alert
        type="info"
        message="当前为 Mock 接口，便于快速理解注册流程"
        description="提交后会提示注册成功并跳转至登录页，不会保存真实数据。"
        show-icon
        class="form-alert"
      />
    </template>

    <!-- 表单内容 -->
    <template #form>
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
        <li>注册成功后，可在"系统设置 → 租户管理"创建测试租户。</li>
      </ul>

      <a-form-item class="form-checkbox">
        <a-checkbox checked disabled>同意 Demo FastAPI 演示环境使用条款</a-checkbox>
      </a-form-item>
    </template>

    <!-- 表单操作按钮 -->
    <template #actions="{ loading }">
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
    </template>
  </AuthPage>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { UserOutlined, MailOutlined, LockOutlined, SafetyOutlined } from '@ant-design/icons-vue'
import AuthPage from '../../components/AuthPage.vue'
import { authApi } from '../../api/auth'

const router = useRouter()
const loading = ref(false)
const form = reactive({
  name: '',
  email: '',
  password: '',
  confirm: ''
})

// 页面配置
const pageConfig = {
  badge: '快速上手',
  title: '创建账号，开启协同治理新旅程',
  description: '注册演示环境，体验统一认证、权限控制与配置治理的完整闭环，快速掌握 Demo FastAPI 的最佳实践。',
  formTitle: '创建新账号',
  formDescription: '完善基础资料，稍后可在个人中心补全部门、角色等信息。',
  meta: '推荐使用企业邮箱注册',
  support: '',
  supportIcon: null
}

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
  transition: all 0.3s ease;
}

.timeline-item:hover {
  background: rgba(131, 24, 67, 0.55);
  border-color: rgba(248, 113, 166, 0.35);
  transform: translateX(4px);
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
  transition: all 0.3s ease;
}

.timeline-item:hover .timeline-index {
  background: rgba(244, 114, 182, 0.45);
  transform: scale(1.05);
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

.form-alert {
  border-radius: 16px;
  background: rgba(255, 240, 246, 0.8);
  border: 1px solid rgba(236, 72, 153, 0.25);
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

/* 输入框聚焦效果 */
:deep(.ant-input:focus),
:deep(.ant-input-focused) {
  border-color: #ec4899;
  box-shadow: 0 0 0 2px rgba(236, 72, 153, 0.1);
}

:deep(.ant-input-password:focus),
:deep(.ant-input-password-focused) {
  border-color: #ec4899;
  box-shadow: 0 0 0 2px rgba(236, 72, 153, 0.1);
}

/* 按钮悬停效果 */
:deep(.ant-btn-primary) {
  background: linear-gradient(135deg, #ec4899, #db2777);
  border: none;
  transition: all 0.3s ease;
}

:deep(.ant-btn-primary:hover) {
  background: linear-gradient(135deg, #db2777, #be185d);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(236, 72, 153, 0.3);
}

@media (max-width: 992px) {
  .form-actions {
    grid-template-columns: repeat(1, minmax(0, 1fr));
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