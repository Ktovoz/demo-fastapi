import { createApp } from "vue"
import Antd from "ant-design-vue"
import App from "./App.vue"
import router from "./router"
import { logger } from "./utils/logger"
import { pinia } from "./store"
import "ant-design-vue/dist/reset.css"

logger.init({
  level: import.meta.env.DEV ? "DEBUG" : "INFO",
  prefix: "Demo FastAPI",
  enableConsole: true,
  enableStorage: true,
  storageKey: "demo_fastapi_logs",
  maxStorageSize: 2000
})

logger.info("Bootstrapping Vue application")

const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(Antd)

app.config.errorHandler = (error, instance, info) => {
  logger.error("Vue global error", {
    error: error.message,
    stack: error.stack,
    component: instance?.$options?.name || "Unknown",
    info
  })
}

app.config.warnHandler = (msg, instance, trace) => {
  logger.warn("Vue warning", {
    message: msg,
    component: instance?.$options?.name || "Unknown",
    trace
  })
}

app.mount("#app")

logger.info("Vue application ready")
