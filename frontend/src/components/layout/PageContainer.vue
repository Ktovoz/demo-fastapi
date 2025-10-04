<template>
  <div class="page-container">
    <div class="page-surface">
      <div v-if="breadcrumbs.length" class="page-breadcrumbs">
        <a-breadcrumb>
          <a-breadcrumb-item v-for="crumb in breadcrumbs" :key="crumb.label">
            <RouterLink v-if="crumb.to" :to="crumb.to">{{ crumb.label }}</RouterLink>
            <span v-else>{{ crumb.label }}</span>
          </a-breadcrumb-item>
        </a-breadcrumb>
      </div>
      <div class="page-header" v-if="title || description || $slots.actions || $slots.extra || $slots.meta">
        <div class="page-header__info">
          <div v-if="$slots.meta" class="page-meta">
            <slot name="meta"></slot>
          </div>
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
  position: relative;
  padding: clamp(20px, 4vw, 40px);
  min-height: calc(100vh - 120px);
  background: linear-gradient(180deg, #f7f9fc 0%, #eef2ff 60%, #f8fafc 100%);
}

.page-surface {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.page-breadcrumbs {
  margin-bottom: 4px;
}

.page-breadcrumbs :deep(.ant-breadcrumb a) {
  color: #2563eb;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  padding: 20px 24px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(226, 232, 240, 0.7);
  box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);
}

.page-header__info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.page-meta {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  color: #2563eb;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.page-title {
  margin: 0;
  font-size: clamp(20px, 3.2vw, 28px);
  font-weight: 600;
  color: #0f172a;
}

.page-description {
  margin: 0;
  max-width: 640px;
  color: #475569;
  font-size: 13px;
  line-height: 1.6;
}

.page-header__actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-content {
  position: relative;
  padding: clamp(20px, 3.6vw, 32px);
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
  border: 1px solid rgba(226, 232, 240, 0.75);
}

@media (max-width: 992px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .page-header__actions {
    justify-content: flex-start;
    flex-wrap: wrap;
  }
}

@media (max-width: 768px) {
  .page-container {
    padding: 18px;
  }

  .page-header {
    border-radius: 16px;
    padding: 18px;
  }

  .page-content {
    border-radius: 18px;
    padding: 18px;
  }
}
</style>
