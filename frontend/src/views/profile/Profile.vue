<template>
  <CardContainer title="个人资料" bordered>
    <a-row :gutter="16">
      <a-col :span="6">
        <UserAvatar :name="profile.name" :size="80" />
        <a-typography-paragraph class="profile-role">{{ profile.role }}</a-typography-paragraph>
        <a-typography-text type="secondary">{{ profile.email }}</a-typography-text>
      </a-col>
      <a-col :span="18">
        <a-descriptions :column="2" bordered>
          <a-descriptions-item label="姓名">{{ profile.name }}</a-descriptions-item>
          <a-descriptions-item label="邮箱">{{ profile.email }}</a-descriptions-item>
          <a-descriptions-item label="角色">{{ profile.role }}</a-descriptions-item>
          <a-descriptions-item label="最后登录">{{ profile.lastLogin || '无' }}</a-descriptions-item>
        </a-descriptions>
      </a-col>
    </a-row>
    <a-divider />
    <a-tabs>
      <a-tab-pane key="general" tab="基本信息">
        <a-form layout="vertical" @finish="saveProfile" :model="form">
          <a-form-item label="显示名称" name="name"><a-input v-model:value="form.name" /></a-form-item>
          <a-form-item label="个人简介" name="bio"><a-textarea v-model:value="form.bio" rows="4" /></a-form-item>
          <a-space>
            <a-button type="primary" html-type="submit" :loading="saving">保存</a-button>
          </a-space>
        </a-form>
      </a-tab-pane>
      <a-tab-pane key="security" tab="安全设置">
        <a-space direction="vertical" style="width: 100%">
          <a-alert type="info" message="模拟环境" description="安全操作在开发阶段仅为模拟演示。" />
          <a-button type="primary" ghost @click="resetPassword">发送重置邮件</a-button>
          <a-checkbox v-model:checked="security.mfa">启用多重身份验证</a-checkbox>
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
    message.success('个人资料已更新（模拟）')
  }, 500)
}

const resetPassword = () => {
  message.success('密码重置邮件已发送（模拟）')
}
</script>

<style scoped>
.profile-role {
  margin-top: 8px;
  font-weight: 600;
}
</style>

