<template>
  <CardContainer title="Profile" bordered>
    <a-row :gutter="16">
      <a-col :span="6">
        <UserAvatar :name="profile.name" :size="80" />
        <a-typography-paragraph class="profile-role">{{ profile.role }}</a-typography-paragraph>
        <a-typography-text type="secondary">{{ profile.email }}</a-typography-text>
      </a-col>
      <a-col :span="18">
        <a-descriptions :column="2" bordered>
          <a-descriptions-item label="Name">{{ profile.name }}</a-descriptions-item>
          <a-descriptions-item label="Email">{{ profile.email }}</a-descriptions-item>
          <a-descriptions-item label="Role">{{ profile.role }}</a-descriptions-item>
          <a-descriptions-item label="Last Login">{{ profile.lastLogin || 'N/A' }}</a-descriptions-item>
        </a-descriptions>
      </a-col>
    </a-row>
    <a-divider />
    <a-tabs>
      <a-tab-pane key="general" tab="General">
        <a-form layout="vertical" @finish="saveProfile" :model="form">
          <a-form-item label="Display Name" name="name"><a-input v-model:value="form.name" /></a-form-item>
          <a-form-item label="Bio" name="bio"><a-textarea v-model:value="form.bio" rows="4" /></a-form-item>
          <a-space>
            <a-button type="primary" html-type="submit" :loading="saving">Save</a-button>
          </a-space>
        </a-form>
      </a-tab-pane>
      <a-tab-pane key="security" tab="Security">
        <a-space direction="vertical" style="width: 100%">
          <a-alert type="info" message="Mock environment" description="Security actions are simulated while backend is in development." />
          <a-button type="primary" ghost @click="resetPassword">Send reset email</a-button>
          <a-checkbox v-model:checked="security.mfa">Enable multi-factor authentication</a-checkbox>
        </a-space>
      </a-tab-pane>
    </a-tabs>
  </CardContainer>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { message } from 'ant-design-vue'
import CardContainer from '../../components/layout/CardContainer.vue'
import UserAvatar from '../../components/business/UserAvatar.vue'
import { useAuthStore } from '../../store/auth'

const authStore = useAuthStore()

const profile = reactive({
  name: authStore.user?.name ?? 'Demo User',
  email: authStore.user?.email ?? 'demo@example.com',
  role: authStore.user?.role ?? 'admin',
  lastLogin: authStore.user?.lastLogin
})

const form = reactive({
  name: profile.name,
  bio: 'Productive admin user'
})

const security = reactive({
  mfa: true
})

const saving = ref(false)

const saveProfile = () => {
  saving.value = true
  setTimeout(() => {
    profile.name = form.name
    saving.value = false
    message.success('Profile updated (mock)')
  }, 500)
}

const resetPassword = () => {
  message.success('Password reset email sent (mock)')
}
</script>

<style scoped>
.profile-role {
  margin-top: 8px;
  font-weight: 600;
}
</style>

