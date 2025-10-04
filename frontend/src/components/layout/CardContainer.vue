<template>
  <a-card
    :bordered="false"
    :hoverable="hoverable"
    :body-style="cardBodyStyle"
    class="card-container"
    :class="cardClasses"
  >
    <template v-if="showHeader" #title>
      <div class="card-header">
        <div class="card-header__main">
          <div v-if="hasIconSlot" class="card-header__icon">
            <slot name="icon"></slot>
          </div>
          <div class="card-header__text">
            <slot name="title">
              <span class="card-header__title">{{ title }}</span>
            </slot>
            <p v-if="description" class="card-header__description">
              {{ description }}
            </p>
          </div>
        </div>
      </div>
    </template>
    <template v-if="showHeaderActions" #extra>
      <div class="card-header__actions">
        <slot name="extra"></slot>
        <a-button
          v-if="collapsible"
          type="text"
          size="small"
          class="collapse-button"
          @click="toggle"
        >
          <span>{{ collapsed ? '展开' : '收起' }}</span>
          <component :is="collapsed ? DownOutlined : UpOutlined" />
        </a-button>
      </div>
    </template>
    <div v-if="hasActionsSlot" class="card-actions">
      <slot name="actions"></slot>
    </div>
    <transition name="fade">
      <div v-show="!collapsed" class="card-body" :style="{ padding: contentPadding }">
        <slot></slot>
      </div>
    </transition>
  </a-card>
</template>

<script setup>
import { computed, ref, watch, useSlots } from 'vue'
import { DownOutlined, UpOutlined } from '@ant-design/icons-vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  bordered: {
    type: Boolean,
    default: false
  },
  collapsible: {
    type: Boolean,
    default: false
  },
  defaultCollapsed: {
    type: Boolean,
    default: false
  },
  hoverable: {
    type: Boolean,
    default: true
  },
  bodyPadding: {
    type: String,
    default: 'clamp(22px, 3vw, 32px)'
  }
})

const slots = useSlots()

const collapsed = ref(props.defaultCollapsed)

watch(
  () => props.defaultCollapsed,
  (value) => {
    collapsed.value = value
  }
)

const hasIconSlot = computed(() => Boolean(slots.icon))
const hasTitleSlot = computed(() => Boolean(slots.title))
const hasActionsSlot = computed(() => Boolean(slots.actions))
const showHeaderActions = computed(() => props.collapsible || Boolean(slots.extra))
const showHeader = computed(
  () =>
    Boolean(
      props.title ||
        props.description ||
        hasTitleSlot.value ||
        hasIconSlot.value ||
        showHeaderActions.value
    )
)

const cardBodyStyle = computed(() => ({
  padding: '0'
}))

const contentPadding = computed(() => props.bodyPadding)

const cardClasses = computed(() => ({
  'card-container--collapsed': collapsed.value,
  'card-container--borderless': !props.bordered
}))

const toggle = () => {
  collapsed.value = !collapsed.value
}
</script>

<style scoped>
.card-container {
  position: relative;
  border-radius: clamp(18px, 2.6vw, 22px);
  background: var(--surface-card);
  border: 1px solid rgba(148, 163, 184, 0.18);
  box-shadow: var(--shadow-soft);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card-container::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 80% 12%, rgba(59, 130, 246, 0.18), transparent 65%);
  opacity: 0.35;
  pointer-events: none;
}

.card-container:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

.card-container--collapsed {
  box-shadow: var(--shadow-soft);
}

.card-container :deep(.ant-card) {
  border-radius: inherit;
  background: transparent;
}

.card-container :deep(.ant-card-body) {
  padding: 0;
  position: relative;
  z-index: 1;
}

.card-container :deep(.ant-card-head) {
  padding: clamp(16px, 2.6vw, 24px) clamp(18px, 2.8vw, 28px) 0;
  border: none;
  background: transparent;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.card-header__main {
  display: flex;
  align-items: center;
  gap: 16px;
}

.card-header__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 14px;
  background: rgba(37, 99, 235, 0.12);
  color: var(--brand-primary);
}

.card-header__text {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.card-header__title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.card-header__description {
  margin: 0;
  font-size: 13px;
  color: var(--text-secondary);
}

.card-header__actions {
  display: inline-flex;
  align-items: center;
  gap: 12px;
}

.collapse-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--brand-primary);
}

.card-actions {
  padding: 0 clamp(18px, 2.6vw, 28px) clamp(12px, 2vw, 18px);
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-body {
  position: relative;
  z-index: 1;
  padding: 0 clamp(18px, 2.6vw, 28px) clamp(22px, 3vw, 32px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .card-container {
    border-radius: 16px;
  }

  .card-body {
    padding: 0 18px 24px;
  }
}
</style>
