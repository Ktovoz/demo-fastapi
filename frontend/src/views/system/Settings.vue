<template>
  <CardContainer title="System Settings" bordered>
    <a-form layout="vertical" @finish="handleSubmit">
      <a-form-item label="Application Name" name="appName">
        <a-input v-model:value="form.appName" />
      </a-form-item>
      <a-form-item label="Default Language" name="language">
        <a-select v-model:value="form.language" :options="languageOptions" />
      </a-form-item>
      <a-form-item label="Theme" name="theme">
        <a-radio-group v-model:value="form.theme">
          <a-radio value="light">Light</a-radio>
          <a-radio value="dark">Dark</a-radio>
        </a-radio-group>
      </a-form-item>
      <a-form-item label="Notifications" name="notifications">
        <a-switch v-model:checked="form.notifications" />
      </a-form-item>
      <a-space>
        <a-button @click="reset">Reset</a-button>
        <a-button type="primary" html-type="submit" :loading="loading">Save</a-button>
      </a-space>
    </a-form>
  </CardContainer>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { message } from 'ant-design-vue'
import CardContainer from '../../components/layout/CardContainer.vue'

const loading = ref(false)
const languageOptions = [
  { label: 'English', value: 'en' },
  { label: '中文', value: 'zh' }
]

const form = reactive({
  appName: 'Demo FastAPI',
  language: 'en',
  theme: 'light',
  notifications: true
})

const handleSubmit = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    message.success('Settings saved (mock)')
  }, 500)
}

const reset = () => {
  form.appName = 'Demo FastAPI'
  form.language = 'en'
  form.theme = 'light'
  form.notifications = true
}
</script>
