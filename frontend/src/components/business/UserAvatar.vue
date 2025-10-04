<template>
  <a-avatar :size="size" :src="src">
    <template v-if="!src">{{ initials }}</template>
  </a-avatar>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    default: ''
  },
  src: {
    type: String,
    default: ''
  },
  size: {
    type: [Number, String],
    default: 40
  }
})

const initials = computed(() => {
  if (!props.name) return 'U'
  const parts = props.name.split(' ')
  return parts.map((p) => p.charAt(0).toUpperCase()).slice(0, 2).join('')
})
</script>
