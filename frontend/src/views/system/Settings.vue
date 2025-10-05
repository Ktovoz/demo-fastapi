<template>
  <div class="system-settings">
    <CardContainer
      title="系统设置"
      description="统一管理后台可见的品牌信息、通知策略与安全参数"
      :body-padding="'24px'"
    >
      <template #icon>
        <div class="settings-icon">
          <SettingOutlined />
        </div>
      </template>

      <a-alert
        message="提示"
        description="更改配置会立即生效，建议在非高峰期间操作，并同步通知相关团队。"
        type="info"
        show-icon
        class="settings-alert"
      />

      <div class="settings-layout">
        <div class="settings-main">
          <a-form layout="vertical" @finish="handleSubmit" :model="form">
            <section class="settings-section">
              <header>
                <h3>基础信息</h3>
                <p>影响导航标题、邮件抬头等对外展示内容。</p>
              </header>
              <a-row :gutter="16">
                <a-col :xs="24" :md="12">
                  <a-form-item label="应用名称" name="appName">
                    <a-input v-model:value="form.appName" placeholder="Demo FastAPI Platform" />
                  </a-form-item>
                </a-col>
                <a-col :xs="24" :md="12">
                  <a-form-item label="默认语言" name="language">
                    <a-select v-model:value="form.language" :options="languageOptions" />
                  </a-form-item>
                </a-col>
              </a-row>
              <a-row :gutter="16">
                <a-col :xs="24" :md="12">
                  <a-form-item label="默认时区" name="timezone">
                    <a-input v-model:value="form.timezone" />
                  </a-form-item>
                </a-col>
                <a-col :xs="24" :md="12">
                  <a-form-item label="主题风格" name="theme">
                    <a-segmented
                      v-model:value="form.theme"
                      :options="themeOptions"
                    />
                  </a-form-item>
                </a-col>
              </a-row>
            </section>

            <section class="settings-section">
              <header>
                <h3>通知策略</h3>
                <p>选择需要同步的渠道，保持关键事件提醒及时触达。</p>
              </header>
              <a-row :gutter="16">
                <a-col :span="8">
                  <a-card bordered class="notify-card" hoverable>
                    <div class="notify-card__header">
                      <MailOutlined />
                      <span>邮件</span>
                    </div>
                    <p>用于投递管理层摘要、日常提醒。</p>
                    <a-switch v-model:checked="form.notifications.email" />
                  </a-card>
                </a-col>
                <a-col :span="8">
                  <a-card bordered class="notify-card" hoverable>
                    <div class="notify-card__header">
                      <MessageOutlined />
                      <span>短信</span>
                    </div>
                    <p>用于突发告警、密码重置等敏感场景。</p>
                    <a-switch v-model:checked="form.notifications.sms" />
                  </a-card>
                </a-col>
                <a-col :span="8">
                  <a-card bordered class="notify-card" hoverable>
                    <div class="notify-card__header">
                      <BellOutlined />
                      <span>站内提醒</span>
                    </div>
                    <p>展示在控制台右上角通知中心。</p>
                    <a-switch v-model:checked="form.notifications.inApp" />
                  </a-card>
                </a-col>
              </a-row>
            </section>

            <section class="settings-section">
              <header>
                <h3>安全策略</h3>
                <p>合理的会话与密码策略可以降低账号被盗风险。</p>
              </header>
              <a-row :gutter="16">
                <a-col :xs="24" :md="12">
                  <a-form-item label="多因素校验">
                    <a-switch v-model:checked="form.security.mfa" />
                    <span class="inline-hint">开启后，敏感操作将强制二次验证。</span>
                  </a-form-item>
                </a-col>
                <a-col :xs="24" :md="12">
                  <a-form-item label="会话超时">
                    <a-input-number
                      v-model:value="form.security.sessionTimeout"
                      :min="5"
                      :max="240"
                      addon-after="分钟"
                      style="width: 220px"
                    />
                  </a-form-item>
                </a-col>
              </a-row>
              <a-form-item label="密码策略">
                <a-textarea v-model:value="form.security.passwordPolicy" rows="3" placeholder="如：至少 12 位，包含大小写、数字与特殊字符" />
              </a-form-item>
            </section>

            <!-- 系统管理功能（管理员及超级管理员） -->
            <section v-if="authStore.user?.is_superuser || authStore.user?.roles?.includes('admin') || authStore.user?.email === 'admin@example.com'" class="settings-section">
              <header>
                <h3 style="color: #ff4d4f;">
                  <WarningOutlined style="margin-right: 8px;" />
                  系统管理
                </h3>
                <p>系统维护和初始化功能，仅超级管理员可访问。</p>
              </header>

              <a-alert
                message="危险操作区域"
                description="以下操作将影响整个系统，请谨慎操作"
                type="warning"
                show-icon
                style="margin-bottom: 24px"
              />

              <a-row :gutter="16">
                <a-col :xs="24" :md="12">
                  <a-form-item label="系统状态">
                    <a-spin :spinning="systemStore.systemStatus === null">
                      <div v-if="systemStore.systemStatus" style="padding: 12px; background: #f5f5f5; border-radius: 6px; font-size: 13px;">
                        <p><strong>数据库状态:</strong> {{ systemStore.systemStatus.database_status }}</p>
                        <p><strong>用户总数:</strong> {{ systemStore.systemStatus.total_users }}</p>
                        <p><strong>角色总数:</strong> {{ systemStore.systemStatus.total_roles }}</p>
                        <p><strong>系统版本:</strong> {{ systemStore.systemStatus.version }}</p>
                        <p><strong>初始化时间:</strong> {{ systemStore.systemStatus.initialized_at ? dayjs(systemStore.systemStatus.initialized_at).format('YYYY-MM-DD HH:mm:ss') : '未知' }}</p>
                      </div>
                      <a-button v-else type="link" @click="fetchSystemStatus">
                        获取系统状态
                      </a-button>
                    </a-spin>
                  </a-form-item>
                </a-col>
                <a-col :xs="24" :md="12">
                  <a-form-item label="定时任务状态">
                    <a-spin :spinning="systemStore.schedulerStatus === null">
                      <div v-if="systemStore.schedulerStatus" style="padding: 12px; background: #f5f5f5; border-radius: 6px; font-size: 13px;">
                        <p><strong>调度器状态:</strong> {{ systemStore.schedulerStatus.is_running ? '运行中' : '已停止' }}</p>
                        <p><strong>下次执行时间:</strong> {{ systemStore.schedulerStatus.next_run ? dayjs(systemStore.schedulerStatus.next_run).format('YYYY-MM-DD HH:mm:ss') : '未知' }}</p>
                        <p><strong>已注册任务:</strong> {{ systemStore.schedulerStatus.tasks?.join(', ') || '无' }}</p>
                      </div>
                      <a-button v-else type="link" @click="fetchSchedulerStatus">
                        获取调度器状态
                      </a-button>
                    </a-spin>
                  </a-form-item>
                </a-col>
              </a-row>

              <a-form-item label="系统初始化">
                <a-space direction="vertical" style="width: 100%">
                  <a-button
                    danger
                    @click="showResetConfirm"
                    :loading="systemStore.resetLoading"
                    :disabled="systemStore.resetLoading"
                  >
                    <template #icon><ReloadOutlined /></template>
                    重置系统到初始状态
                  </a-button>
                  <a-text type="secondary" style="font-size: 12px;">
                    清除所有业务数据并重置系统到初始状态（仅保留基础角色和管理员账户）
                    <br>
                    系统会在每天0点自动执行此操作
                  </a-text>
                </a-space>
              </a-form-item>
            </section>

            <div class="settings-actions">
              <a-button @click="reset">还原</a-button>
              <a-button type="primary" html-type="submit" :loading="saving">保存设置</a-button>
            </div>
          </a-form>
        </div>

        <aside class="settings-side">
          <a-card bordered class="side-card" :hoverable="false">
            <h4>当前配置速览</h4>
            <ul>
              <li><span>语言</span><strong>{{ languageLabel }}</strong></li>
              <li><span>主题</span><strong>{{ themeLabel }}</strong></li>
              <li><span>通知渠道</span><strong>{{ activeChannels.join(' / ') }}</strong></li>
              <li><span>会话超时</span><strong>{{ form.security.sessionTimeout }} 分钟</strong></li>
            </ul>
          </a-card>

          <a-card bordered class="side-card" :hoverable="false">
            <h4>操作建议</h4>
            <ol>
              <li>在保存前确认配置是否同步至文档。</li>
              <li>更改主题后通知前端同步调色板。</li>
              <li>安全策略调整建议与安全团队确认。</li>
            </ol>
          </a-card>
        </aside>
      </div>
    </CardContainer>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { message, Modal } from 'ant-design-vue'
import dayjs from 'dayjs'
import CardContainer from '../../components/layout/CardContainer.vue'
import { useSystemStore } from '../../store/system'
import { useAuthStore } from '../../store/auth'
import { createLogger } from '../../utils/logger'
import {
  BellOutlined,
  MailOutlined,
  MessageOutlined,
  SettingOutlined,
  WarningOutlined,
  ReloadOutlined
} from '@ant-design/icons-vue'

const systemStore = useSystemStore()
const authStore = useAuthStore()
const saving = ref(false)
const logger = createLogger('Settings')

const form = reactive({
  appName: '',
  language: 'en',
  timezone: 'UTC',
  theme: 'light',
  notifications: { email: true, sms: false, inApp: true },
  security: { mfa: true, sessionTimeout: 30, passwordPolicy: '' }
})

const languageOptions = [
  { label: '英文', value: 'en' },
  { label: '中文', value: 'zh' }
]

const themeOptions = [
  { label: '亮色', value: 'light' },
  { label: '暗色', value: 'dark' }
]

const loadSettings = async () => {
  try {
    await systemStore.fetchSettings()
    if (systemStore.settings) {
      Object.assign(form, JSON.parse(JSON.stringify(systemStore.settings)))
    }
  } catch (error) {
    message.error('读取系统设置失败')
  }
}

const handleSubmit = async () => {
  saving.value = true
  try {
    await systemStore.updateSettings(JSON.parse(JSON.stringify(form)))
    message.success('已保存系统设置')
  } catch (error) {
    message.error('保存失败，请稍后再试')
  } finally {
    saving.value = false
  }
}

const reset = () => {
  loadSettings()
}

const languageLabel = computed(() => languageOptions.find((item) => item.value === form.language)?.label ?? form.language)
const themeLabel = computed(() => themeOptions.find((item) => item.value === form.theme)?.label ?? form.theme)
const activeChannels = computed(() => {
  const channels = []
  if (form.notifications.email) channels.push('邮件')
  if (form.notifications.sms) channels.push('短信')
  if (form.notifications.inApp) channels.push('站内')
  return channels.length ? channels : ['已全部关闭']
})

// 获取系统状态
const fetchSystemStatus = async () => {
  try {
    await systemStore.fetchSystemStatus()
    message.success('获取系统状态成功')
  } catch (error) {
    console.error('获取系统状态失败:', error)
    message.error('获取系统状态失败: ' + (error.message || '请检查网络连接'))
  }
}

// 获取调度器状态
const fetchSchedulerStatus = async () => {
  try {
    await systemStore.fetchSchedulerStatus()
    message.success('获取调度器状态成功')
  } catch (error) {
    console.error('获取调度器状态失败:', error)
    message.error('获取调度器状态失败: ' + (error.message || '请检查网络连接'))
  }
}

// 显示系统重置确认对话框
const showResetConfirm = () => {
  Modal.confirm({
    title: '确认重置系统',
    content: '此操作将清除所有业务数据并重置系统到初始状态，仅保留基础角色和管理员账户。此操作不可恢复，是否继续？',
    okText: '确认重置',
    cancelText: '取消',
    okType: 'danger',
    onOk: async () => {
      try {
        await systemStore.resetSystem()
        message.success('系统重置成功')
        // 重新获取系统状态
        fetchSystemStatus()
      } catch (error) {
        message.error('系统重置失败')
      }
    }
  })
}

onMounted(async () => {
  loadSettings()

  // 检查并修复admin权限
  if (authStore.user?.email === 'admin@example.com' && !authStore.user?.is_superuser) {
    try {
      logger.info("检测到admin用户缺少superuser权限，尝试修复...")
      await systemStore.fixAdminSuperuser()
      // 重新获取用户信息
      await authStore.restoreSession()
      message.success("admin权限已修复")
    } catch (error) {
      logger.error("自动修复admin权限失败:", error)
    }
  }

  // 如果是超级管理员或管理员，自动获取系统状态
  if (authStore.user?.is_superuser || authStore.user?.email === 'admin@example.com') {
    fetchSystemStatus()
    fetchSchedulerStatus()
  }
})
</script>

<style scoped>
.system-settings {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.settings-icon {
  width: 46px;
  height: 46px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  color: #fff;
  background: linear-gradient(135deg, #0ea5e9, #2563eb);
}

.settings-alert {
  margin-bottom: 20px;
}

.settings-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 300px;
  gap: 20px;
}

.settings-section {
  margin-bottom: 24px;
  padding: 18px;
  border-radius: 18px;
  background: rgba(248, 250, 252, 0.8);
  border: 1px solid rgba(226, 232, 240, 0.7);
}

.settings-section header {
  margin-bottom: 14px;
}

.settings-section h3 {
  margin: 0 0 4px;
  font-size: 16px;
  color: #0f172a;
}

.settings-section p {
  margin: 0;
  font-size: 12px;
  color: #64748b;
}

.notify-card {
  min-height: 158px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 12px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: none;
}

.notify-card__header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #0f172a;
}

.inline-hint {
  display: block;
  margin-top: 8px;
  font-size: 12px;
  color: #94a3b8;
}

.settings-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 18px;
}

.settings-side {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.side-card {
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.95);
}

.side-card h4 {
  margin: 0 0 12px;
  font-size: 15px;
  color: #0f172a;
}

.side-card ul,
.side-card ol {
  margin: 0;
  padding-left: 18px;
  font-size: 13px;
  color: #475569;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.side-card ul li,
.side-card ol li {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.side-card ul li span {
  color: #94a3b8;
}

@media (max-width: 1024px) {
  .settings-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .settings-section {
    padding: 14px;
  }
}
</style>
