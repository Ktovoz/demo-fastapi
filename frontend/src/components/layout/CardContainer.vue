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
    default: '20px'
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
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.92), rgba(241, 245, 249, 0.88));
  border: 1px solid rgba(148, 163, 184, 0.2);
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  overflow: hidden;
}

.card-container--borderless {
  border-color: transparent;
  box-shadow: 0 10px 28px rgba(148, 163, 184, 0.12);
}

.card-container:hover {
  transform: translateY(-4px);
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12);
}

.card-container::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(59, 130, 246, 0.14), transparent 55%);
  pointer-events: none;
  opacity: 0.9;
}

.card-container--collapsed {
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
}

.card-container :deep(.ant-card) {
  border-radius: 20px;
  overflow: hidden;
}

.card-container :deep(.ant-card-head) {
  padding: 18px 24px 0;
  border-bottom: none;
  background: transparent;
  min-height: auto;
}

.card-container :deep(.ant-card-head-title) {
  padding: 0;
}

.card-container :deep(.ant-card-extra) {
  padding: 0;
}

.card-container :deep(.ant-card-body) {
  padding: 0;
  position: relative;
  z-index: 1;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-header__main {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-header__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.14), rgba(59, 130, 246, 0.05));
  color: #1d4ed8;
}

.card-header__text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.card-header__title {
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
}

.card-header__description {
  margin: 0;
  font-size: 12px;
  color: #64748b;
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
  color: #1d4ed8;
}

.collapse-button :deep(.anticon) {
  font-size: 12px;
}

.card-actions {
  padding: 0 24px 16px;
}

.card-body {
  position: relative;
  z-index: 1;
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
    border-radius: 18px;
  }

  .card-container :deep(.ant-card-head) {
    padding: 16px 18px 0;
  }

  .card-actions {
    padding: 0 18px 14px;
  }
}
</style>