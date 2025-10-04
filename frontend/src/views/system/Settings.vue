<template>
  <CardContainer title="System Settings" bordered>
    <a-form layout="vertical" @finish="handleSubmit" :model="form">
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="Application Name" name="appName">
            <a-input v-model:value="form.appName" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="Default Language" name="language">
            <a-select v-model:value="form.language" :options="languageOptions" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item label="Timezone" name="timezone">
        <a-input v-model:value="form.timezone" />
      </a-form-item>
      <a-form-item label="Theme" name="theme">
        <a-radio-group v-model:value="form.theme">
          <a-radio value="light">Light</a-radio>
          <a-radio value="dark">Dark</a-radio>
        </a-radio-group>
      </a-form-item>
      <a-row :gutter="16">
        <a-col :span="8">
          <a-form-item label="Email Notifications">
            <a-switch v-model:checked="form.notifications.email" />
          </a-form-item>
        </a-col>
        <a-col :span="8">
          <a-form-item label="SMS Notifications">
            <a-switch v-model:checked="form.notifications.sms" />
          </a-form-item>
        </a-col>
        <a-col :span="8">
          <a-form-item label="In-App Notifications">
            <a-switch v-model:checked="form.notifications.inApp" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item label="Security">
        <a-space direction="vertical" style="width: 100%">
          <a-checkbox v-model:checked="form.security.mfa">Require MFA</a-checkbox>
          <a-input-number
            v-model:value="form.security.sessionTimeout"
            :min="5"
            :max="240"
            addon-after="mins"
            style="width: 200px"
          />
          <a-textarea v-model:value="form.security.passwordPolicy" rows="3" />
        </a-space>
      </a-form-item>
      <a-space>
        <a-button @click="reset">Reset</a-button>
        <a-button type="primary" html-type="submit" :loading="saving">Save</a-button>
      </a-space>
    </a-form>
  </CardContainer>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { message } from 'ant-design-vue'
import CardContainer from '../../components/layout/CardContainer.vue'
import { useSystemStore } from '../../store/system'

const systemStore = useSystemStore()
const saving = ref(false)

const form = reactive({
  appName: '',
  language: 'en',
  timezone: 'UTC',
  theme: 'light',
  notifications: { email: true, sms: false, inApp: true },
  security: { mfa: true, sessionTimeout: 30, passwordPolicy: '' }
})

const languageOptions = [
  { label: 'English', value: 'en' },
  { label: '中文', value: 'zh' }
]

const loadSettings = async () => {
  try {
    await systemStore.fetchSettings()
    if (systemStore.settings) {
      Object.assign(form, JSON.parse(JSON.stringify(systemStore.settings)))
    }
  } catch (error) {
    message.error('Failed to load settings')
  }
}

const handleSubmit = async () => {
  saving.value = true
  try {
    await systemStore.updateSettings(JSON.parse(JSON.stringify(form)))
    message.success('Settings saved')
  } catch (error) {
    message.error('Failed to save settings')
  } finally {
    saving.value = false
  }
}

const reset = () => {
  loadSettings()
}

onMounted(loadSettings)
</script>

