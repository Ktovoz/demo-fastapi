<template>
  <CardContainer title="Profile" bordered>
    <a-row :gutter="16">
      <a-col :span="6">
        <UserAvatar :name="profile.name" :size="80" />
      </a-col>
      <a-col :span="18">
        <a-descriptions :column="1" bordered>
          <a-descriptions-item label="Name">{{ profile.name }}</a-descriptions-item>
          <a-descriptions-item label="Email">{{ profile.email }}</a-descriptions-item>
          <a-descriptions-item label="Role">{{ profile.role }}</a-descriptions-item>
        </a-descriptions>
      </a-col>
    </a-row>
    <a-divider />
    <a-form layout="vertical" @finish="handleSubmit">
      <a-form-item label="Display Name" name="name">
        <a-input v-model:value="form.name" />
      </a-form-item>
      <a-form-item label="Bio" name="bio">
        <a-textarea v-model:value="form.bio" rows="4" />
      </a-form-item>
      <a-button type="primary" html-type="submit">Update Profile</a-button>
    </a-form>
  </CardContainer>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { message } from 'ant-design-vue'
import CardContainer from '../../components/layout/CardContainer.vue'
import UserAvatar from '../../components/business/UserAvatar.vue'

const profile = ref({
  name: 'Demo User',
  email: 'demo@example.com',
  role: 'admin'
})

const form = reactive({
  name: profile.value.name,
  bio: 'Productive admin user'
})

const handleSubmit = () => {
  message.success('Profile updated (mock)')
}
</script>
