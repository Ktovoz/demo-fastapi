<template>
  <div class="page-body" :class="bodyClasses">
    <slot />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  gap: {
    type: [Number, String],
    default: 24
  },
  bleed: {
    type: Boolean,
    default: false
  }
})

const bodyClasses = computed(() => ({
  'page-body--bleed': props.bleed
}))
</script>

<style scoped>
.page-body {
  display: flex;
  flex-direction: column;
  gap: var(--page-body-gap, clamp(20px, 3vw, 32px));
}

.page-body--bleed {
  margin: 0 calc(-1 * clamp(20px, 3vw, 40px));
}
</style>
