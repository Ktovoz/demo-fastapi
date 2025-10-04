<template>
  <header class="page-header" :class="headerClasses">
    <div class="page-header__main">
      <div v-if="$slots.meta" class="page-header__meta">
        <slot name="meta" />
      </div>
      <div class="page-header__titles">
        <slot name="title">
          <h1 v-if="title" class="page-header__title">{{ title }}</h1>
        </slot>
        <slot name="description">
          <p v-if="description" class="page-header__description">{{ description }}</p>
        </slot>
      </div>
      <div v-if="breadcrumbs?.length" class="page-header__breadcrumbs">
        <slot name="breadcrumbs">
          <a-breadcrumb>
            <a-breadcrumb-item v-for="crumb in breadcrumbs" :key="crumb.label">
              <RouterLink v-if="crumb.to" :to="crumb.to">{{ crumb.label }}</RouterLink>
              <span v-else>{{ crumb.label }}</span>
            </a-breadcrumb-item>
          </a-breadcrumb>
        </slot>
      </div>
    </div>
    <div v-if="$slots.actions || $slots.extra" class="page-header__actions">
      <slot name="actions" />
      <slot name="extra" />
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  align: {
    type: String,
    default: 'start'
  },
  condensed: {
    type: Boolean,
    default: false
  },
  breadcrumbs: {
    type: Array,
    default: () => []
  }
})

const headerClasses = computed(() => ({
  'page-header--center': props.align === 'center',
  'page-header--condensed': props.condensed
}))
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: clamp(16px, 2.4vw, 28px);
  padding: clamp(20px, 3.2vw, 32px);
  border-radius: clamp(16px, 2.8vw, 26px);
  background: var(--surface-elevated);
  border: 1px solid rgba(148, 163, 184, 0.24);
  box-shadow: var(--shadow-soft);
  backdrop-filter: blur(14px);
}

.page-header--condensed {
  padding: clamp(16px, 2.2vw, 24px);
  border-radius: clamp(14px, 2.4vw, 20px);
}

.page-header__main {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.page-header__meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--brand-primary);
}

.page-header__title {
  margin: 0;
  color: var(--text-primary);
  font-size: clamp(24px, 3.8vw, 32px);
  font-weight: 600;
}

.page-header__description {
  margin: 0;
  max-width: 680px;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.page-header__actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.page-header__breadcrumbs {
  font-size: 12px;
  color: rgba(79, 70, 229, 0.85);
}

.page-header--center {
  align-items: center;
  text-align: center;
}

.page-header--center .page-header__actions {
  justify-content: center;
}

@media (max-width: 992px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .page-header__actions {
    justify-content: flex-start;
  }
}
</style>
