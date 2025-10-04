<template>
  <a-card :title="title" :bordered="bordered" class="card-container">
    <template #extra>
      <slot name="extra"></slot>
    </template>
    <slot></slot>
  </a-card>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  bordered: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.card-container {
  width: 100%;
}
</style>
