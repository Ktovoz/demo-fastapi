<template>
  <div class="page-container">
    <div v-if="breadcrumbs.length" class="page-breadcrumbs">
      <a-breadcrumb>
        <a-breadcrumb-item v-for="crumb in breadcrumbs" :key="crumb.label">
          <RouterLink v-if="crumb.to" :to="crumb.to">{{ crumb.label }}</RouterLink>
          <span v-else>{{ crumb.label }}</span>
        </a-breadcrumb-item>
      </a-breadcrumb>
    </div>
    <div class="page-header" v-if="title || description || $slots.actions || $slots.extra">
      <div class="page-header__info">
        <h1 class="page-title">{{ title }}</h1>
        <p class="page-description" v-if="description">{{ description }}</p>
      </div>
      <div class="page-header__actions">
        <slot name="actions"></slot>
        <slot name="extra"></slot>
      </div>
    </div>
    <div class="page-content">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { RouterLink } from "vue-router"

const props = defineProps({
  title: {
    type: String,
    default: ""
  },
  description: {
    type: String,
    default: ""
  },
  breadcrumbs: {
    type: Array,
    default: () => []
  }
})

const breadcrumbs = computed(() => props.breadcrumbs ?? [])
</script>

<style scoped>
.page-container {
  padding: 24px;
  min-height: calc(100vh - 120px);
}

.page-breadcrumbs {
  margin-bottom: 12px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  gap: 16px;
}

.page-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.page-description {
  margin: 4px 0 0;
  color: rgba(0, 0, 0, 0.45);
}

.page-header__actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-content {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}
</style>
