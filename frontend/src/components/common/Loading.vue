<template>
  <div class="loading" :class="{ overlay }">
    <a-spin :tip="tip" />
  </div>
</template>

<script setup>
const props = defineProps({
  tip: {
    type: String,
    default: 'Loading...'
  },
  overlay: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.loading.overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.65);
  z-index: 10;
}
</style>
