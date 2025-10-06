import axios from "axios"
import { API_CONFIG } from "../config/api"
import { createApiLogger } from "./logger"
import { useAuthStore } from "../store/auth"
import { pinia } from "../store"

const apiLogger = createApiLogger()

console.log('🔧 Axios: 开始创建axios实例');
console.log('🔧 Axios: 使用的API_CONFIG:', API_CONFIG);

const api = axios.create({
  ...API_CONFIG
})

console.log('🔧 Axios: axios实例创建完成');
console.log('🔧 Axios: axios实例baseURL:', api.defaults.baseURL);

api.interceptors.request.use(
  (config) => {
    console.log('🚀 Axios Request: 发送请求');
    console.log('🚀 Axios Request: 完整URL:', config.baseURL + config.url);
    console.log('🚀 Axios Request: 方法:', config.method?.toUpperCase());
    console.log('🚀 Axios Request: baseURL:', config.baseURL);
    console.log('🚀 Axios Request: 相对URL:', config.url);
    console.log('🚀 Axios Request: 请求头:', config.headers);
    console.log('🚀 Axios Request: 请求数据:', config.data);

    const authStore = useAuthStore(pinia)
    if (authStore?.token) {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${authStore.token}`
      }
      console.log('🚀 Axios Request: 已添加认证头');
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
    console.log('✅ Axios Response: 收到响应');
    console.log('✅ Axios Response: 状态码:', response.status);
    console.log('✅ Axios Response: 请求URL:', response.config?.baseURL + response.config?.url);
    console.log('✅ Axios Response: 响应数据:', response.data);

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
    console.log('❌ Axios Error: 请求失败');
    console.log('❌ Axios Error: 请求URL:', error.config?.baseURL + error.config?.url);
    console.log('❌ Axios Error: 错误信息:', error.message);
    console.log('❌ Axios Error: 状态码:', error.response?.status);
    console.log('❌ Axios Error: 响应数据:', error.response?.data);
    console.log('❌ Axios Error: 错误详情:', error);

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
