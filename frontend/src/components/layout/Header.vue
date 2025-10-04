<template>
  <a-layout-header class="layout-header">
    <div class="brand">
      <slot name="logo">Demo Admin</slot>
      <span class="page-title">{{ pageTitle }}</span>
    </div>
    <div class="header-actions">
      <slot name="actions"></slot>
    </div>
  </a-layout-header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// Provide simple page title derived from route meta
const pageTitle = computed(() => route.meta?.title || 'Dashboard')
</script>

<style scoped>
.layout-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: #001529;
  color: #fff;
}

.brand {
  display: flex;
  align-items: center;
  gap: 16px;
  font-weight: 600;
  font-size: 18px;
}

.page-title {
  font-size: 16px;
  opacity: 0.8;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}
</style>
