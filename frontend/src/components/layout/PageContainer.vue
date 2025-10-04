<template>
  <PageSurface :padded="padded" :full-height="fullHeight" class="page-container">
    <template v-if="$slots.background" #background>
      <slot name="background" />
    </template>

    <PageHeader
      v-if="showHeader"
      :title="title"
      :description="description"
      :breadcrumbs="breadcrumbs"
      :align="headerAlign"
      :condensed="condensed"
    >
      <template v-if="$slots.meta" #meta>
        <slot name="meta" />
      </template>
      <template v-if="$slots.breadcrumbs" #breadcrumbs>
        <slot name="breadcrumbs" />
      </template>
      <template v-if="$slots.title" #title>
        <slot name="title" />
      </template>
      <template v-if="$slots.description" #description>
        <slot name="description" />
      </template>
      <template v-if="$slots.actions" #actions>
        <slot name="actions" />
      </template>
      <template v-if="$slots.extra" #extra>
        <slot name="extra" />
      </template>
    </PageHeader>

    <PageBody :class="bodyClasses" :style="bodyStyle">
      <slot />
    </PageBody>
  </PageSurface>
</template>

<script setup>
import { computed, useSlots } from 'vue'
import PageSurface from './PageSurface.vue'
import PageHeader from './PageHeader.vue'
import PageBody from './PageBody.vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  breadcrumbs: {
    type: Array,
    default: () => []
  },
  hideHeader: {
    type: Boolean,
    default: false
  },
  padded: {
    type: Boolean,
    default: true
  },
  fullHeight: {
    type: Boolean,
    default: false
  },
  condensed: {
    type: Boolean,
    default: false
  },
  headerAlign: {
    type: String,
    default: 'start'
  },
  bodyBleed: {
    type: Boolean,
    default: false
  },
  bodyGap: {
    type: [Number, String],
    default: 24
  }
})

const slots = useSlots()

const breadcrumbs = computed(() => props.breadcrumbs ?? [])

const showHeader = computed(() => {
  if (props.hideHeader) return false
  return (
    props.title ||
    props.description ||
    breadcrumbs.value.length > 0 ||
    Boolean(slots.meta || slots.actions || slots.extra || slots.title || slots.description)
  )
})

const bodyClasses = computed(() => ({
  'page-container__body--bleed': props.bodyBleed
}))

const bodyStyle = computed(() => ({
  '--page-body-gap': typeof props.bodyGap === 'number' ? `${props.bodyGap}px` : props.bodyGap
}))
</script>

<style scoped>
.page-container {
  position: relative;
  min-height: calc(100vh - var(--header-height, 64px));
  background: linear-gradient(180deg, #f7f9fc 0%, #eef2ff 60%, #f8fafc 100%);
  border-radius: clamp(18px, 3vw, 28px);
}

.page-container__body--bleed {
  margin: 0 calc(-1 * clamp(20px, 3vw, 40px));
}
</style>
