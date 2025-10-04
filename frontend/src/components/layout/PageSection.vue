<template>
  <section class="page-section" :class="sectionClasses">
    <header v-if="hasHeader" class="page-section__header">
      <div class="page-section__heading">
        <div v-if="icon || $slots.icon" class="page-section__icon">
          <slot name="icon">
            <component :is="icon" v-if="icon" />
          </slot>
        </div>
        <div class="page-section__text">
          <slot name="header">
            <h2 v-if="title" class="page-section__title">{{ title }}</h2>
            <p v-if="description" class="page-section__description">{{ description }}</p>
          </slot>
        </div>
      </div>
      <div v-if="$slots.actions" class="page-section__actions">
        <slot name="actions" />
      </div>
    </header>

    <div class="page-section__content">
      <template v-if="layout === 'split'">
        <div class="page-section__split">
          <div class="page-section__split-main">
            <slot />
          </div>
          <aside class="page-section__split-aside">
            <slot name="aside" />
          </aside>
        </div>
      </template>
      <template v-else-if="layout === 'grid'">
        <div class="page-section__grid" :style="gridStyle">
          <slot />
        </div>
      </template>
      <template v-else>
        <slot />
      </template>
    </div>
  </section>
</template>

<script setup>
import { computed, useSlots } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  icon: {
    type: [String, Object],
    default: null
  },
  layout: {
    type: String,
    default: 'default'
  },
  columns: {
    type: Number,
    default: 3
  },
  gap: {
    type: [Number, String],
    default: 16
  }
})

const hasHeader = computed(() => props.title || props.description || !!props.icon || !!slots.header || !!slots.actions)
const slots = useSlots()

const sectionClasses = computed(() => ({
  [`page-section--${props.layout}`]: true
}))

const gridStyle = computed(() => ({
  '--page-section-grid-columns': props.columns,
  '--page-section-grid-gap': typeof props.gap === 'number' ? `${props.gap}px` : props.gap
}))
</script>

<style scoped>
.page-section {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.page-section__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.page-section__heading {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-section__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 12px;
  background: rgba(37, 99, 235, 0.12);
  color: #2563eb;
}

.page-section__title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
}

.page-section__description {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 13px;
}

.page-section__actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-section__split {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: 20px;
}

.page-section__split-aside {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.page-section__grid {
  display: grid;
  grid-template-columns: repeat(var(--page-section-grid-columns, 3), minmax(0, 1fr));
  gap: var(--page-section-grid-gap, 16px);
}

@media (max-width: 1200px) {
  .page-section__split {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .page-section__grid {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}
</style>

