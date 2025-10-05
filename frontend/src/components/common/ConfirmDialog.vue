<template>
  <a-modal
    :open="open"
    :title="title"
    :confirm-loading="loading"
    :ok-text="okText"
    :cancel-text="cancelText"
    :ok-type="okType"
    :mask-closable="maskClosable"
    @ok="handleOk"
    @cancel="handleCancel"
  >
    <slot>您确定要继续吗？</slot>
  </a-modal>
</template>

<script setup>
const emit = defineEmits(['update:open', 'confirm', 'cancel'])

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: '确认'
  },
  loading: {
    type: Boolean,
    default: false
  },
  okText: {
    type: String,
    default: '确认'
  },
  cancelText: {
    type: String,
    default: '取消'
  },
  okType: {
    type: String,
    default: 'primary'
  },
  maskClosable: {
    type: Boolean,
    default: false
  }
})

const handleOk = () => {
  emit('confirm')
}

const handleCancel = () => {
  emit('cancel')
  emit('update:open', false)
}
</script>

