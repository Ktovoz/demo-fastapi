<template>
  <div class="error-page">
    <a-result status="403" title="访问被拒绝" sub-title="您没有权限访问此页面。">
      <template #extra>
        <a-space>
          <a-button type="primary" @click="requestAccess">申请权限</a-button>
          <a-button @click="goBack">返回</a-button>
        </a-space>
      </template>
    </a-result>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const requestAccess = () => {
  // Placeholder for access request
  router.push('/profile')
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.error-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}
</style>
