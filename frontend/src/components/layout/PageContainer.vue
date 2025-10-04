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
  padding: clamp(24px, 5vw, 48px);
  min-height: calc(100vh - 120px);
  background: radial-gradient(circle at 20% 15%, rgba(59, 130, 246, 0.12), transparent 60%),
    radial-gradient(circle at 80% 0%, rgba(14, 165, 233, 0.08), transparent 55%),
    linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
}

.page-container::after {
  content: '';
  position: absolute;
  inset: clamp(12px, 2vw, 24px);
  border-radius: 32px;
  border: 1px solid rgba(148, 163, 184, 0.16);
  pointer-events: none;
  opacity: 0.5;
}

.page-surface {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-breadcrumbs {
  margin-bottom: 4px;
}

.page-breadcrumbs :deep(.ant-breadcrumb a) {
  color: #1d4ed8;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
  padding: 24px 28px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(148, 163, 184, 0.16);
  box-shadow: 0 14px 38px rgba(15, 23, 42, 0.08);
}

.page-header__info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.page-meta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #1d4ed8;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.page-title {
  margin: 0;
  font-size: clamp(22px, 4vw, 30px);
  font-weight: 600;
  color: #0f172a;
}

.page-description {
  margin: 0;
  max-width: 680px;
  color: #475569;
  font-size: 14px;
  line-height: 1.7;
}

.page-header__actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-content {
  position: relative;
  padding: clamp(24px, 4vw, 36px);
  background: rgba(255, 255, 255, 0.9);
  border-radius: 28px;
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.1);
  border: 1px solid rgba(148, 163, 184, 0.18);
}

.page-content::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 28px;
  background: radial-gradient(circle at 85% 15%, rgba(59, 130, 246, 0.12), transparent 60%);
  pointer-events: none;
}

@media (max-width: 992px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
    padding: 20px 24px;
  }

  .page-header__actions {
    justify-content: flex-start;
    flex-wrap: wrap;
  }
}

@media (max-width: 768px) {
  .page-container {
    padding: 20px;
  }

  .page-container::after {
    inset: 12px;
    border-radius: 24px;
  }

  .page-header {
    border-radius: 20px;
  }

  .page-content {
    border-radius: 22px;
    padding: 20px;
  }
}
</style>
