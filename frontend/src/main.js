import { createApp } from "vue"
import Antd from "ant-design-vue"
import App from "./App.vue"
import router from "./router"
import { logger } from "./utils/logger"
import { pinia } from "./store"
import "ant-design-vue/dist/reset.css"

// 初始化日志系统
logger.info("开始初始化日志系统")
logger.init({
  level: import.meta.env.DEV ? "DEBUG" : "INFO",
  prefix: "Demo FastAPI",
  enableConsole: true,
  enableStorage: true,
  storageKey: "demo_fastapi_logs",
  maxStorageSize: 2000
})

logger.info("日志系统初始化完成")

// 检查环境信息
logger.info("环境信息:", {
  mode: import.meta.env.MODE,
  dev: import.meta.env.DEV,
  prod: import.meta.env.PROD,
  baseUrl: import.meta.env.BASE_URL
})

logger.info("开始创建Vue应用实例")
const app = createApp(App)

logger.info("开始注册插件")

// 注册Pinia状态管理
logger.info("注册Pinia状态管理")
app.use(pinia)

// 注册Vue Router
logger.info("注册Vue Router")
app.use(router)

// 注册Ant Design Vue
logger.info("注册Ant Design Vue")
app.use(Antd)

// 全局错误处理器
app.config.errorHandler = (error, instance, info) => {
  logger.error("Vue全局错误:", {
    error: error.message,
    stack: error.stack,
    component: instance?.$options?.name || "Unknown",
    info
  })
}

// 全局警告处理器
app.config.warnHandler = (msg, instance, trace) => {
  logger.warn("Vue警告:", {
    message: msg,
    component: instance?.$options?.name || "Unknown",
    trace
  })
}

// 添加未捕获的Promise错误处理
window.addEventListener('unhandledrejection', (event) => {
  logger.error("未捕获的Promise拒绝:", {
    reason: event.reason,
    promise: event.promise
  })
})

// 添加全局错误处理
window.addEventListener('error', (event) => {
  logger.error("全局错误:", {
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    error: event.error
  })
})

logger.info("准备挂载应用到DOM")
app.mount("#app")

logger.info("🎉 Vue应用启动完成!")

// 开发环境下添加额外的调试信息
if (import.meta.env.DEV) {
  logger.info("开发模式调试信息:", {
    appVersion: app.version,
    vueVersion: app.version,
    antdVersion: Antd.version
  })
}
