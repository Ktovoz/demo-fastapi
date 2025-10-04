<template>
  <a-table
    :columns="columns"
    :data-source="dataSource"
    :row-key="rowKey"
    :loading="loading"
    :row-selection="rowSelection"
    :pagination="internalPagination"
    :scroll="scroll"
    :locale="{ emptyText }"
    @change="handleChange"
  >
    <template v-for="(_, name) in $slots" :key="name" v-slot:[name]="slotProps">
      <slot :name="name" v-bind="slotProps"></slot>
    </template>
  </a-table>
</template>

<script setup>
import { computed } from 'vue'

const emit = defineEmits(['change'])

const props = defineProps({
  columns: {
    type: Array,
    default: () => []
  },
  dataSource: {
    type: Array,
    default: () => []
  },
  rowKey: {
    type: [String, Function],
    default: 'id'
  },
  loading: {
    type: Boolean,
    default: false
  },
  rowSelection: {
    type: [Object, null],
    default: null
  },
  pagination: {
    type: [Object, Boolean, null],
    default: false
  },
  emptyText: {
    type: String,
    default: 'No data'
  },
  scroll: {
    type: [Object, null],
    default: null
  }
})

const internalPagination = computed(() => (props.pagination === null ? undefined : props.pagination))

const handleChange = (pagination, filters, sorter, extra) => {
  emit('change', pagination, filters, sorter, extra)
}
</script>
