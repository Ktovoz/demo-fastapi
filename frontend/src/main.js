import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'
import App from './App.vue'
import router from './router'
import { logger } from './utils/logger'
import 'ant-design-vue/dist/reset.css'

// 初始化日志系统
logger.init({
  level: import.meta.env.DEV ? 'DEBUG' : 'INFO',
  prefix: 'Demo FastAPI',
  enableConsole: true,
  enableStorage: true,
  storageKey: 'demo_fastapi_logs',
  maxStorageSize: 2000
})

logger.info('🚀 开始初始化 Vue 应用')

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Antd)

// 全局错误处理
app.config.errorHandler = (error, instance, info) => {
  logger.error('🚨 Vue 全局错误:', {
    error: error.message,
    stack: error.stack,
    component: instance?.$options?.name || 'Unknown',
    info
  })
}

// 全局警告处理
app.config.warnHandler = (msg, instance, trace) => {
  logger.warn('⚠️ Vue 警告:', {
    message: msg,
    component: instance?.$options?.name || 'Unknown',
    trace
  })
}

app.mount('#app')

logger.info('✅ Vue 应用初始化完成')