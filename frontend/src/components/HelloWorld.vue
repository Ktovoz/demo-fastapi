<template>
  <div class="hello-world">
    <a-card title="Hello World 组件" :bordered="false">
      <p>{{ message }}</p>
      <a-space>
        <a-button type="primary" @click="increment">点击次数: {{ count }}</a-button>
        <a-button @click="reset">重置</a-button>
      </a-space>
    </a-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '../store/counter'

defineProps({
  message: {
    type: String,
    default: '这是一个示例组件'
  }
})

const counterStore = useCounterStore()
const count = computed(() => counterStore.count)

const increment = () => {
  counterStore.increment()
}

const reset = () => {
  counterStore.reset()
}
</script>

<style scoped>
.hello-world {
  margin: 20px 0;
}
</style>