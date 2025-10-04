<template>
  <a-card :title="title" :bordered="bordered" class="card-container">
    <template #extra>
      <a-space align="center">
        <slot name="extra"></slot>
        <a-button
          v-if="collapsible"
          type="text"
          size="small"
          @click="toggle"
        >
          <span v-if="collapsed">Expand</span>
          <span v-else>Collapse</span>
        </a-button>
      </a-space>
    </template>
    <div v-if="$slots.actions" class="card-actions">
      <slot name="actions"></slot>
    </div>
    <transition name="fade">
      <div v-show="!collapsed">
        <slot></slot>
      </div>
    </transition>
  </a-card>
</template>

<script setup>
import { ref, watch } from "vue"

const props = defineProps({
  title: {
    type: String,
    default: ""
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
  }
})

const collapsed = ref(props.defaultCollapsed)

watch(
  () => props.defaultCollapsed,
  (value) => {
    collapsed.value = value
  }
)

const toggle = () => {
  collapsed.value = !collapsed.value
}
</script>

<style scoped>
.card-container {
  width: 100%;
}

.card-actions {
  margin-bottom: 16px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
