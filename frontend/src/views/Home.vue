<template>
  <div class="home">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card title="欢迎使用 FastAPI + Vue Demo" :bordered="false">
          <p>这是一个前后端分离的示例项目，使用以下技术栈：</p>
          <ul>
            <li>前端：Vue 3 + Ant Design Vue + Vite</li>
            <li>后端：FastAPI + Python</li>
          </ul>
          <a-space>
            <a-button type="primary" @click="testAPI">测试后端API</a-button>
            <a-button @click="goToAbout">了解更多</a-button>
          </a-space>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" style="margin-top: 16px;">
      <a-col :span="12">
        <a-card title="API 响应" :bordered="false">
          <div v-if="loading">
            <a-spin />
          </div>
          <div v-else>
            <p v-if="apiResponse">{{ apiResponse }}</p>
            <p v-else>点击"测试后端API"按钮测试连接</p>
          </div>
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-card title="项目信息" :bordered="false">
          <p><strong>项目名称：</strong>Demo FastAPI</p>
          <p><strong>版本：</strong>v1.0.0</p>
          <p><strong>开发环境：</strong>Development</p>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { api } from '../utils/api'

const router = useRouter()
const loading = ref(false)
const apiResponse = ref('')

const testAPI = async () => {
  loading.value = true
  try {
    const response = await api.get('/')
    apiResponse.value = `连接成功！后端返回：${JSON.stringify(response.data)}`
    message.success('API 连接成功！')
  } catch (error) {
    console.error('API 测试失败:', error)
    apiResponse.value = `连接失败：${error.message}`
    message.error('API 连接失败，请检查后端服务是否启动')
  } finally {
    loading.value = false
  }
}

const goToAbout = () => {
  router.push('/about')
}
</script>

<style scoped>
.home {
  padding: 20px;
}
</style>