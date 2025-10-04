import axios from 'axios'
import { logger } from './logger'

// 延迟创建API日志器，避免在模块加载时就创建
let apiLogger = null

const getApiLogger = () => {
  if (!apiLogger) {
    // 简单的API日志器，不依赖复杂的初始化
    apiLogger = {
      request: (method, url, data = null) => {
        console.log(`[API] 📤 发送请求: ${method.toUpperCase()} ${url}`)
        if (data) {
          console.log('[API] 📦 请求数据:', data)
        }
      },

      response: (method, url, status, data = null, duration = null) => {
        const durationText = duration ? ` | 耗时: ${duration}ms` : ''
        console.log(`[API] 📥 收到响应: ${method.toUpperCase()} ${url} | 状态码: ${status}${durationText}`)
        if (data) {
          console.log('[API] 📦 响应数据:', data)
        }
      },

      error: (method, url, error, duration = null) => {
        const durationText = duration ? ` | 耗时: ${duration}ms` : ''
        console.error(`[API] ❌ 请求失败: ${method.toUpperCase()} ${url} | 错误: ${error}${durationText}`)
      }
    }
  }
  return apiLogger
}

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api', // 通过 Vite 代理到后端
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const startTime = performance.now()
    config.metadata = { startTime }

    // 记录请求日志
    getApiLogger().request(
      config.method || 'GET',
      config.url || '',
      config.data
    )

    return config
  },
  error => {
    getApiLogger().error('REQUEST', '', error.message)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    const endTime = performance.now()
    const duration = (endTime - response.config.metadata.startTime).toFixed(0)

    // 记录响应日志
    getApiLogger().response(
      response.config.method || 'GET',
      response.config.url || '',
      response.status,
      response.data,
      duration
    )

    return response
  },
  error => {
    const endTime = performance.now()
    let duration = 0

    if (error.config?.metadata?.startTime) {
      duration = (endTime - error.config.metadata.startTime).toFixed(0)
    }

    let errorMessage = error.message
    let statusCode = null

    if (error.response) {
      // 服务器返回了错误状态码
      statusCode = error.response.status
      errorMessage = `HTTP ${statusCode}: ${error.response.data?.detail || error.response.data?.message || error.message}`
    } else if (error.request) {
      // 请求已发出但没有收到响应
      errorMessage = '网络请求失败，请检查网络连接'
    } else {
      // 设置请求时发生了错误
      errorMessage = `请求配置错误: ${error.message}`
    }

    getApiLogger().error(
      error.config?.method || 'GET',
      error.config?.url || '',
      errorMessage,
      duration
    )

    return Promise.reject(error)
  }
)

// 便捷方法
const apiRequest = {
  get: (url, config) => {
    return api.get(url, config)
  },
  post: (url, data, config) => {
    return api.post(url, data, config)
  },
  put: (url, data, config) => {
    return api.put(url, data, config)
  },
  delete: (url, config) => {
    return api.delete(url, config)
  },
  patch: (url, data, config) => {
    return api.patch(url, data, config)
  }
}

export { api, apiRequest }