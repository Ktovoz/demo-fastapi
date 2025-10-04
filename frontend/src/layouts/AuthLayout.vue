<template>
  <div class="auth-layout">
    <div class="auth-card">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
// Simple auth layout wrapper
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #dfe9f3 0%, #ffffff 100%);
  padding: 24px;
}

.auth-card {
  width: 100%;
  max-width: 420px;
}
</style>
