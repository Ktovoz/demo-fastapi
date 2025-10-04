<template>
  <CardContainer title="User Detail" bordered>
    <a-descriptions bordered :column="1">
      <a-descriptions-item label="Name">{{ user.name }}</a-descriptions-item>
      <a-descriptions-item label="Email">{{ user.email }}</a-descriptions-item>
      <a-descriptions-item label="Role">{{ user.role }}</a-descriptions-item>
      <a-descriptions-item label="Status">{{ user.status }}</a-descriptions-item>
      <a-descriptions-item label="Created At">{{ user.createdAt }}</a-descriptions-item>
    </a-descriptions>
    <a-space style="margin-top: 16px;">
      <a-button @click="goBack">Back</a-button>
      <a-button type="primary" @click="editUser">Edit</a-button>
    </a-space>
  </CardContainer>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CardContainer from '../../components/layout/CardContainer.vue'

const router = useRouter()
const route = useRoute()

const user = computed(() => ({
  id: route.params.id,
  name: 'Mock User',
  email: 'mock@example.com',
  role: 'admin',
  status: 'Active',
  createdAt: '2025-10-01'
}))

const goBack = () => {
  router.push('/users/list')
}

const editUser = () => {
  router.push(`/users/${route.params.id}/edit`)
}
</script>
