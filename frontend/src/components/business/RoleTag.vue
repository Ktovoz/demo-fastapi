<template>
  <a-tag :color="colorMap[role] || 'blue'">
    <slot>{{ role }}</slot>
  </a-tag>
</template>

<script setup>
const props = defineProps({
  role: {
    type: String,
    default: 'user'
  }
})

const colorMap = {
  admin: 'red',
  manager: 'gold',
  user: 'blue',
  guest: 'default'
}
</script>
