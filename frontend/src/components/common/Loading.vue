<template>
  <div :class="wrapperClass">
    <a-spin :tip="tip" :size="size" />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  tip: {
    type: String,
    default: '加载中...'
  },
  overlay: {
    type: Boolean,
    default: false
  },
  fullscreen: {
    type: Boolean,
    default: false
  },
  size: {
    type: String,
    default: 'default'
  }
})

const wrapperClass = computed(() => ({
  loading: true,
  overlay: props.overlay,
  fullscreen: props.fullscreen
}))
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

.loading.fullscreen {
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0.75);
  z-index: 1000;
}
</style>

