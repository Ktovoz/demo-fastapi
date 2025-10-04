<template>
  <AuthLayout>
    <a-card class="auth-card" :bordered="false" :class="themeClass">
      <a-row class="auth-card__content" :gutter="0">
        <!-- 左侧介绍区域 -->
        <a-col :xs="24" :lg="10" class="auth-card__intro">
          <div class="intro-pattern intro-pattern--one"></div>
          <div class="intro-pattern intro-pattern--two"></div>
          <div class="intro-top">
            <div class="intro-badge">
              <span class="badge-dot"></span>
              {{ config.badge }}
            </div>
            <h2 class="intro-title">{{ config.title }}</h2>
            <p class="intro-text">{{ config.description }}</p>
          </div>

          <!-- 左侧特色内容插槽 -->
          <div class="intro-features">
            <slot name="features"></slot>
          </div>

          <div class="intro-footer">
            <div class="intro-meta">
              <span>作者：ktovoz</span>
              <span class="divider">|</span>
              <span>{{ config.meta }}</span>
            </div>
            <span class="intro-support" v-if="config.support">
              <component :is="config.supportIcon" />
              {{ config.support }}
            </span>
          </div>
        </a-col>

        <!-- 右侧表单区域 -->
        <a-col :xs="24" :lg="14" class="auth-card__form">
          <div class="form-panel">
            <div class="form-header">
              <h3>{{ config.formTitle }}</h3>
              <p>{{ config.formDescription }}</p>
            </div>

            <!-- 表单提示信息插槽 -->
            <slot name="alert"></slot>

    <!-- 表单内容插槽 -->
    <div class="form-container">
      <a-form
        layout="vertical"
        @finish="handleSubmit"
        :model="formModel"
        class="form-body"
      >
        <slot name="form"></slot>

        <!-- 表单操作按钮插槽 -->
        <div class="form-actions-wrapper">
          <slot name="actions" :loading="loading"></slot>
        </div>
      </a-form>
    </div>
          </div>
        </a-col>
      </a-row>
    </a-card>
  </AuthLayout>
</template>

<script setup>
import { computed } from 'vue'
import AuthLayout from '../layouts/AuthLayout.vue'

const props = defineProps({
  // 主题配置
  theme: {
    type: String,
    default: 'blue', // blue, pink, green
    validator: (value) => ['blue', 'pink', 'green'].includes(value)
  },
  // 页面配置
  config: {
    type: Object,
    required: true,
    validator: (value) => {
      const required = ['badge', 'title', 'description', 'formTitle', 'formDescription', 'meta']
      return required.every(key => key in value)
    }
  },
  // 表单数据模型
  formModel: {
    type: Object,
    required: true
  },
  // 加载状态
  loading: {
    type: Boolean,
    default: false
  }
})

// 主题样式类
const themeClass = computed(() => `auth-card--${props.theme}`)

// 表单提交处理
const emit = defineEmits(['submit'])

const handleSubmit = () => {
  emit('submit')
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
}

/* 主题样式 */
.auth-card--blue {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(59, 130, 246, 0.12));
}

.auth-card--pink {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(248, 113, 166, 0.08));
  box-shadow: 0 42px 88px rgba(190, 24, 93, 0.18);
}

.auth-card--green {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(34, 197, 94, 0.12));
  box-shadow: 0 42px 88px rgba(15, 92, 42, 0.18);
}

.auth-card__content {
  min-height: 480px;
  align-items: stretch;
}

/* 主题 - 蓝色 */
.auth-card--blue .auth-card__intro {
  background: radial-gradient(circle at 20% 16%, rgba(59, 130, 246, 0.35), transparent 60%),
    radial-gradient(circle at 80% 75%, rgba(37, 99, 235, 0.25), transparent 58%),
    linear-gradient(210deg, #1e3a8a 0%, #3b82f6 48%, #1e3a8a 100%);
  color: #e0e7ff;
}

.auth-card--blue .intro-text {
  color: rgba(224, 231, 255, 0.88);
}

.auth-card--blue .intro-footer {
  color: rgba(224, 231, 255, 0.78);
}

.auth-card--blue .intro-pattern--one {
  background: rgba(96, 165, 250, 0.55);
}

.auth-card--blue .intro-pattern--two {
  background: rgba(37, 99, 235, 0.45);
}

.auth-card--blue .intro-badge {
  background: rgba(30, 58, 138, 0.28);
  border: 1px solid rgba(224, 231, 255, 0.25);
  color: rgba(224, 231, 255, 0.88);
}

.auth-card--blue .badge-dot {
  background: linear-gradient(135deg, #60a5fa, #3b82f6);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25);
}

.auth-card--blue .step-icon {
  background: rgba(59, 130, 246, 0.25);
  color: #93c5fd;
}

.auth-card--blue .intro-support .anticon {
  color: #93c5fd;
}

.auth-card--blue .auth-card__form {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.94) 0%, rgba(240, 249, 255, 0.9) 100%);
}

.auth-card--blue .form-header h3 {
  color: #1e3a8a;
}

/* 主题 - 粉色 */
.auth-card--pink .auth-card__intro {
  background: radial-gradient(circle at 24% 18%, rgba(251, 113, 133, 0.4), transparent 60%),
    radial-gradient(circle at 75% 82%, rgba(244, 114, 182, 0.35), transparent 55%),
    linear-gradient(210deg, #9d174d 0%, #be123c 52%, #831843 100%);
  color: #fff1f2;
}

.auth-card--pink .intro-text {
  color: rgba(255, 241, 242, 0.85);
}

.auth-card--pink .intro-footer {
  color: rgba(255, 241, 242, 0.8);
}

.auth-card--pink .intro-pattern--one {
  background: rgba(253, 164, 175, 0.65);
}

.auth-card--pink .intro-pattern--two {
  background: rgba(244, 114, 182, 0.55);
}

.auth-card--pink .intro-badge {
  background: rgba(131, 24, 67, 0.6);
  border: 1px solid rgba(255, 228, 230, 0.35);
  color: rgba(255, 241, 242, 0.9);
}

.auth-card--pink .badge-dot {
  background: linear-gradient(135deg, #f9a8d4, #f472b6);
  box-shadow: 0 0 0 2px rgba(244, 114, 182, 0.25);
}

.auth-card--pink .timeline-index {
  background: rgba(244, 114, 182, 0.35);
  color: #fff7fb;
}

.auth-card--pink .auth-card__form {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.94) 0%, rgba(255, 247, 253, 0.94) 100%);
}

.auth-card--pink .form-header h3 {
  color: #831843;
}

/* 主题 - 绿色 */
.auth-card--green .auth-card__intro {
  background: radial-gradient(circle at 22% 15%, rgba(34, 197, 94, 0.35), transparent 60%),
    radial-gradient(circle at 78% 82%, rgba(16, 185, 129, 0.25), transparent 58%),
    linear-gradient(210deg, #064e3b 0%, #047857 48%, #064e3b 100%);
  color: #d1fae5;
}

.auth-card--green .intro-text {
  color: rgba(209, 250, 229, 0.88);
}

.auth-card--green .intro-footer {
  color: rgba(209, 250, 229, 0.78);
}

.auth-card--green .intro-pattern--one {
  background: rgba(74, 222, 128, 0.55);
}

.auth-card--green .intro-pattern--two {
  background: rgba(16, 185, 129, 0.45);
}

.auth-card--green .intro-badge {
  background: rgba(6, 78, 59, 0.6);
  border: 1px solid rgba(209, 250, 229, 0.35);
  color: rgba(209, 250, 229, 0.9);
}

.auth-card--green .badge-dot {
  background: linear-gradient(135deg, #4ade80, #22c55e);
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.25);
}

.auth-card--green .metric-card strong {
  color: #ecfdf5;
}

.auth-card--green .auth-card__form {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.94) 0%, rgba(240, 253, 244, 0.9) 100%);
}

.auth-card--green .form-header h3 {
  color: #064e3b;
}

/* 通用样式 */
.auth-card__intro {
  position: relative;
  padding: 42px 36px;
  display: flex;
  flex-direction: column;
  gap: 28px;
  isolation: isolate;
  overflow: hidden;
}

/* 统一的表单输入框样式 */
.form-input {
  border-radius: 12px;
  border: 1.5px solid #e2e8f0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 15px;
  padding: 14px 16px;
  background: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.form-input:hover {
  border-color: #cbd5e1;
  background-color: #f8fafc;
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.08);
}

.form-input:focus,
.form-input-focused {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
  background-color: #ffffff;
  transform: translateY(-1px);
}

/* 统一的按钮样式 */
.submit-btn {
  border-radius: 10px;
  height: 48px;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
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
  width: 200px;
  height: 200px;
  top: -70px;
  right: -50px;
}

.intro-pattern--two {
  width: 260px;
  height: 260px;
  bottom: -100px;
  left: -90px;
}

.intro-top,
.intro-features,
.intro-footer {
  position: relative;
  z-index: 1;
}

.intro-top {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.intro-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 14px;
  border-radius: 999px;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.badge-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.intro-title {
  margin: 0;
  font-size: 26px;
  line-height: 1.3;
  color: #f8fafc;
  font-weight: 600;
  letter-spacing: 0.01em;
}

.intro-text {
  margin: 0;
  font-size: 13px;
  line-height: 1.6;
  color: rgba(224, 231, 255, 0.88);
  letter-spacing: 0.005em;
}

.intro-footer {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  gap: 8px;
}

.intro-meta {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.intro-meta .divider {
  opacity: 0.6;
}

.intro-support {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 10px;
}

.auth-card__form {
  position: relative;
  padding: 54px 62px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.form-panel {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-header h3 {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
}

.form-header p {
  margin: 6px 0 0;
  color: #64748b;
  line-height: 1.6;
}

.form-container {
  position: relative;
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-actions-wrapper {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid rgba(226, 232, 240, 0.6);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .auth-card {
    border-radius: 24px;
  }

  .auth-card__intro {
    padding: 36px 32px;
    gap: 24px;
  }

  .intro-top {
    gap: 12px;
  }

  .intro-title {
    font-size: 24px;
  }

  .intro-text {
    font-size: 12px;
  }

  .auth-card__form {
    padding: 42px 40px;
  }
}

@media (max-width: 992px) {
  .auth-card__form {
    padding: 36px 28px 40px;
  }

  .auth-card__intro {
    padding: 32px 28px;
    gap: 22px;
  }

  .intro-title {
    font-size: 22px;
  }

  .intro-text {
    font-size: 12px;
  }

  .form-actions-wrapper {
    margin-top: 12px;
    padding-top: 12px;
  }
}

@media (max-width: 768px) {
  .auth-card {
    border-radius: 20px;
  }

  .auth-card__intro {
    padding: 28px 24px;
    gap: 20px;
  }

  .intro-top {
    gap: 10px;
  }

  .intro-title {
    font-size: 20px;
    line-height: 1.25;
  }

  .intro-text {
    font-size: 12px;
    line-height: 1.5;
  }

  .intro-footer {
    font-size: 10px;
  }

  .auth-card__form {
    padding: 28px 24px 32px;
  }

  .form-actions-wrapper {
    margin-top: 16px;
    padding-top: 16px;
  }
}

@media (max-width: 576px) {
  .auth-card {
    border-radius: 16px;
  }

  .auth-card__intro {
    padding: 24px 20px;
    gap: 18px;
  }

  .auth-card__form {
    padding: 24px 20px 28px;
  }

  .intro-title {
    font-size: 18px;
    line-height: 1.3;
  }

  .intro-text {
    font-size: 11px;
    line-height: 1.5;
  }

  .form-actions-wrapper {
    margin-top: 20px;
    padding-top: 20px;
  }
}
</style>