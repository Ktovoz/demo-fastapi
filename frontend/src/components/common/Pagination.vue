<template>
  <a-pagination
    :current="current"
    :page-size="pageSize"
    :total="total"
    :show-size-changer="showSizeChanger"
    :show-quick-jumper="showQuickJumper"
    :simple="simple"
    :show-total="showTotal ? (total) => `Total ${total}` : undefined"
    @change="handleChange"
    @showSizeChange="handleSizeChange"
  />
</template>

<script setup>
const emit = defineEmits(['update:current', 'update:pageSize', 'change'])

const props = defineProps({
  current: {
    type: Number,
    default: 1
  },
  pageSize: {
    type: Number,
    default: 10
  },
  total: {
    type: Number,
    default: 0
  },
  showSizeChanger: {
    type: Boolean,
    default: true
  },
  showQuickJumper: {
    type: Boolean,
    default: true
  },
  showTotal: {
    type: Boolean,
    default: true
  },
  simple: {
    type: Boolean,
    default: false
  }
})

const handleChange = (page, size) => {
  emit('update:current', page)
  emit('change', { page, pageSize: size })
}

const handleSizeChange = (page, size) => {
  emit('update:pageSize', size)
  emit('change', { page, pageSize: size })
}
</script>

