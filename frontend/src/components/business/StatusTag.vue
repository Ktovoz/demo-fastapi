<template>
  <a-tag :color="statusColor">
    <slot>{{ statusLabel }}</slot>
  </a-tag>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    default: 'active'
  }
})

const statusMap = {
  active: { color: 'green', label: 'Active' },
  inactive: { color: 'default', label: 'Inactive' },
  pending: { color: 'orange', label: 'Pending' },
  blocked: { color: 'red', label: 'Blocked' }
}

const statusColor = computed(() => statusMap[props.status]?.color || 'default')
const statusLabel = computed(() => statusMap[props.status]?.label || props.status)
</script>
