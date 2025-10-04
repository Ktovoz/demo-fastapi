<template>
  <a-form :model="localValues" layout="inline" @submit.prevent="handleSubmit">
    <template v-for="item in items" :key="item.key">
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
        <a-button type="primary" html-type="submit">Search</a-button>
        <a-button @click="handleReset">Reset</a-button>
        <slot name="extra"></slot>
      </a-space>
    </a-form-item>
  </a-form>
</template>

<script setup>
import { reactive, watch } from 'vue'

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

const localValues = reactive({ ...props.modelValue })

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
