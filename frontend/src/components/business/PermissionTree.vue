<template>
  <a-tree
    checkable
    :tree-data="treeData"
    :checked-keys="checkedKeys"
    @check="handleCheck"
  />
</template>

<script setup>
const emit = defineEmits(['update:checkedKeys', 'change'])

const props = defineProps({
  treeData: {
    type: Array,
    default: () => []
  },
  checkedKeys: {
    type: Array,
    default: () => []
  }
})

const handleCheck = (keys) => {
  emit('update:checkedKeys', keys)
  emit('change', keys)
}
</script>
