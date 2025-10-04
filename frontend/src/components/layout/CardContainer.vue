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
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.97), rgba(248, 250, 252, 0.94));
  border: 1px solid rgba(226, 232, 240, 0.7);
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  overflow: hidden;
}

.card-container--borderless {
  border-color: transparent;
  box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
}

.card-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08);
}

.card-container::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 85% 15%, rgba(59, 130, 246, 0.12), transparent 60%);
  pointer-events: none;
  opacity: 0.55;
}

.card-container--collapsed {
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.06);
}

.card-container :deep(.ant-card) {
  border-radius: 16px;
  overflow: hidden;
}

.card-container :deep(.ant-card-head) {
  padding: 16px 20px 0;
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
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(59, 130, 246, 0.12);
  color: #1d4ed8;
}

.card-header__text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.card-header__title {
  font-size: 15px;
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
  gap: 10px;
}

.collapse-button {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #1d4ed8;
}

.collapse-button :deep(.anticon) {
  font-size: 12px;
}

.card-actions {
  padding: 0 20px 12px;
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
    border-radius: 14px;
  }

  .card-container :deep(.ant-card-head) {
    padding: 14px 16px 0;
  }

  .card-actions {
    padding: 0 16px 12px;
  }
}
</style>
