import axios from "axios"
import { API_CONFIG } from "../config/api"
import { createApiLogger } from "./logger"
import { useAuthStore } from "../store/auth"
import { pinia } from "../store"

const apiLogger = createApiLogger()

const api = axios.create({
  ...API_CONFIG
})

api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore(pinia)
    if (authStore?.token) {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${authStore.token}`
      }
    }

    const startTime = typeof performance !== "undefined" ? performance.now() : Date.now()
    config.metadata = { startTime }

    apiLogger.request(config.method ?? "get", config.url ?? "", config.data)
    return config
  },
  (error) => {
    apiLogger.error("request", error.config?.url ?? "", error.message)
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => {
    const endTime = typeof performance !== "undefined" ? performance.now() : Date.now()
    const duration = response.config?.metadata?.startTime
      ? (endTime - response.config.metadata.startTime).toFixed(0)
      : null

    apiLogger.response(
      response.config?.method ?? "get",
      response.config?.url ?? "",
      response.status,
      response.data,
      duration
    )

    return response
  },
  (error) => {
    const endTime = typeof performance !== "undefined" ? performance.now() : Date.now()
    const start = error.config?.metadata?.startTime
    const duration = start ? (endTime - start).toFixed(0) : null

    const status = error.response?.status
    const message = error.response?.data?.detail || error.response?.data?.message || error.message

    apiLogger.error(error.config?.method ?? "get", error.config?.url ?? "", message, duration)

    if (status === 401) {
      const authStore = useAuthStore(pinia)
      authStore.logout()
    }

    return Promise.reject(error)
  }
)

export const apiRequest = {
  get: (url, config) => api.get(url, config),
  post: (url, data, config) => api.post(url, data, config),
  put: (url, data, config) => api.put(url, data, config),
  delete: (url, config) => api.delete(url, config),
  patch: (url, data, config) => api.patch(url, data, config)
}

export { api }
