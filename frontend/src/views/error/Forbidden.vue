<template>
  <div class="error-page">
    <a-result status="403" title="Access Denied" sub-title="You do not have permission to view this page.">
      <template #extra>
        <a-space>
          <a-button type="primary" @click="requestAccess">Request Access</a-button>
          <a-button @click="goBack">Go Back</a-button>
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
