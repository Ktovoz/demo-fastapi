<template>
  <div class="page-surface" :class="surfaceClasses">
    <div v-if="$slots.background" class="page-surface__background">
      <slot name="background" />
    </div>
    <div class="page-surface__content">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  padded: {
    type: Boolean,
    default: true
  },
  fullHeight: {
    type: Boolean,
    default: false
  }
})

const surfaceClasses = computed(() => ({
  'page-surface--padded': props.padded,
  'page-surface--full-height': props.fullHeight
}))
</script>

<style scoped>
.page-surface {
  position: relative;
  padding: 0;
  min-height: 100%;
}

.page-surface__background {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.page-surface__content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-surface--padded .page-surface__content {
  padding: clamp(20px, 3vw, 40px);
}

.page-surface--full-height {
  min-height: calc(100vh - var(--header-height, 64px));
}
</style>
