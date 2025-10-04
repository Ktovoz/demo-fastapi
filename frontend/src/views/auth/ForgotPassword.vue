<template>
  <AuthPage
    theme="blue"
    :config="pageConfig"
    :form-model="form"
    :loading="loading"
    @submit="handleSubmit"
  >
    <!-- 左侧特色内容 -->
    <template #features>
      <div class="intro-steps">
        <div class="step-item">
          <span class="step-icon">
            <MailOutlined />
          </span>
          <div class="step-content">
            <strong>输入邮箱地址</strong>
            <span>请输入注册时使用的企业邮箱</span>
          </div>
        </div>
        <div class="step-item">
          <span class="step-icon">
            <SafetyOutlined />
          </span>
          <div class="step-content">
            <strong>验证身份信息</strong>
            <span>系统将发送验证链接到您的邮箱</span>
          </div>
        </div>
        <div class="step-item">
          <span class="step-icon">
            <LockOutlined />
          </span>
          <div class="step-content">
            <strong>重置登录密码</strong>
            <span>点击邮件链接设置新密码完成重置</span>
          </div>
        </div>
      </div>
    </template>

    <!-- 表单提示信息 -->
    <template #alert>
      <div class="form-alert">
        <ExclamationCircleOutlined />
        <div class="form-alert__content">
          <strong>安全提醒</strong>
          <span>重置链接有效期为 30 分钟，请及时查收邮件并完成重置。</span>
        </div>
      </div>
    </template>

    <!-- 表单内容 -->
    <template #form>
      <div class="form-field-group">
        <a-form-item
          label="企业邮箱"
          name="email"
          :rules="[{ required: true, message: '请输入邮箱地址' }]"
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

        <ul class="form-tips">
          <li>请确保邮箱地址正确，重置链接将发送至此邮箱</li>
          <li>如未收到邮件，请检查垃圾邮件文件夹</li>
        </ul>
      </div>
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
          class="submit-btn"
        >
          <template #loading>
            <LoadingOutlined spin />
          </template>
          <span class="btn-text">发送重置链接</span>
        </a-button>
        <a-button block size="large" @click="goBack" class="back-btn">
          <span class="btn-text">返回登录</span>
        </a-button>
      </div>
    </template>
  </AuthPage>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import {
  MailOutlined,
  SafetyOutlined,
  LockOutlined,
  SafetyCertificateOutlined,
  ExclamationCircleOutlined,
  LoadingOutlined
} from '@ant-design/icons-vue'
import AuthPage from '../../components/AuthPage.vue'
import { authApi } from '../../api/auth'

const router = useRouter()
const loading = ref(false)
const form = reactive({ email: '' })

// 页面配置
const pageConfig = {
  badge: '安全重置',
  title: '找回您的 Demo FastAPI 账号密码',
  description: '通过企业邮箱验证，快速重置密码。我们采用多层加密保护，确保账号安全与数据隐私。',
  formTitle: '重置密码',
  formDescription: '输入注册邮箱，我们将发送重置链接到您的邮箱，点击链接即可设置新密码。',
  meta: '银行级加密保护',
  support: '安全认证',
  supportIcon: SafetyCertificateOutlined
}

const handleSubmit = async () => {
  loading.value = true
  try {
    await authApi.requestPasswordReset({ email: form.email })
    message.success('重置链接已发送到您的邮箱（演示环境）')
    router.push('/auth/login')
  } catch (error) {
    message.error(error?.message || '发送失败，请重试')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/auth/login')
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

  .form-alert {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 18px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(219, 234, 254, 0.9), rgba(191, 219, 254, 1));
    border: 1.5px solid rgba(59, 130, 246, 0.3);
    color: #1e3a8a;
    backdrop-filter: blur(8px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .form-alert:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
    border-color: rgba(59, 130, 246, 0.4);
  }

  .form-alert .anticon {
    font-size: 20px;
    color: #3b82f6;
    margin-top: 2px;
    transition: all 0.3s ease;
  }

  .form-alert:hover .anticon {
    transform: scale(1.1);
  }

  .form-alert__content {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .form-alert__content strong {
    font-size: 15px;
    color: #1e3a8a;
    font-weight: 600;
  }

  .form-alert__content span {
    font-size: 13px;
    color: #3730a3;
    line-height: 1.5;
  }

.input-icon {
  color: #94a3b8;
}

  .form-tips {
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 6px;
    list-style: none;
    font-size: 13px;
    color: #64748b;
    background: rgba(248, 250, 252, 0.8);
    border-radius: 12px;
    padding: 12px 16px;
    border: 1px solid rgba(226, 232, 240, 0.6);
  }

  .form-tips li {
    position: relative;
    padding-left: 16px;
    line-height: 1.5;
  }

  .form-tips li::before {
    content: "•";
    position: absolute;
    left: 0;
    color: #3b82f6;
    font-weight: bold;
    font-size: 16px;
  }

  .form-field-group {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .form-actions {
    display: grid;
    gap: 12px;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    margin-top: 8px;
  }

  .submit-btn {
    border-radius: 10px;
    height: 48px;
    font-size: 15px;
    font-weight: 500;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .back-btn {
    border-radius: 10px;
    height: 48px;
    font-size: 15px;
    font-weight: 500;
    border: 1px solid #e2e8f0;
    color: #64748b;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .back-btn:hover {
    border-color: #cbd5e1;
    background: #f8fafc;
    color: #334155;
    transform: translateY(-1px);
  }

  .btn-text {
    font-weight: 500;
  }

@media (max-width: 992px) {
  .form-actions {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }

  .form-alert {
    flex-direction: column;
    text-align: center;
    gap: 8px;
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

  .form-actions {
    gap: 8px;
  }

  .submit-btn,
  .back-btn {
    height: 44px;
    font-size: 14px;
  }

  .form-tips {
    padding: 10px 12px;
    font-size: 12px;
  }
}
</style>