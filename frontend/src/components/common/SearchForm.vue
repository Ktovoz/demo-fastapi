<template>
  <a-form :model="localValues" layout="inline" @submit.prevent="handleSubmit" class="search-form">
    <template v-for="item in visibleItems" :key="item.key">
      <a-form-item :label="item.label">
        <component
          :is="item.component || 'a-input'"
          v-model:value="localValues[item.key]"
          v-bind="item.props"
        />
      </a-form-item>
    </template>
    <a-form-item>
      <a-space>
        <a-button type="primary" html-type="submit">搜索</a-button>
        <a-button @click="handleReset">重置</a-button>
        <a-button v-if="advancedItems.length" type="link" @click="advancedOpen = !advancedOpen">
          {{ advancedOpen ? '隐藏高级选项' : '显示高级选项' }}
        </a-button>
        <slot name="extra"></slot>
      </a-space>
    </a-form-item>
  </a-form>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'

const emit = defineEmits(['submit', 'reset', 'update:modelValue'])

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const advancedOpen = ref(false)

const localValues = reactive({ ...props.modelValue })

const basicItems = computed(() => props.items.filter((item) => !item.advanced))
const advancedItems = computed(() => props.items.filter((item) => item.advanced))

const visibleItems = computed(() =>
  advancedOpen.value ? props.items : basicItems.value
)

watch(
  () => props.modelValue,
  (next) => {
    Object.assign(localValues, next)
  },
  { deep: true }
)

watch(
  localValues,
  (next) => {
    emit('update:modelValue', { ...next })
  },
  { deep: true }
)

const handleSubmit = () => {
  emit('submit', { ...localValues })
}

const handleReset = () => {
  Object.keys(localValues).forEach((key) => {
    localValues[key] = undefined
  })
  emit('reset')
  emit('update:modelValue', { ...localValues })
}
</script>

<style scoped>
.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
</style>

