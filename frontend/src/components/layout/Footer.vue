<template>
  <a-layout-footer class="layout-footer">
    <slot>
      Demo FastAPI Admin (c) 2025 Created by Team
    </slot>
  </a-layout-footer>
</template>

<script setup>
// No script logic needed for simple footer
</script>

<style scoped>
.layout-footer {
  text-align: center;
  color: rgba(0, 0, 0, 0.45);
  padding: 16px 24px;
  background: #fff;
  border-top: 1px solid #f0f0f0;
}
</style>
