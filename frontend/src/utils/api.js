import axios from "axios"
import { API_CONFIG, ensureConfigLoaded } from "../config/api"
import { createApiLogger } from "./logger"
import { useAuthStore } from "../store/auth"
import { pinia } from "../store"

const apiLogger = createApiLogger()

// 延迟创建axios实例，确保配置已加载
let axiosInstance = null

const getApiInstance = () => {
  if (!axiosInstance) {
    console.log('🔧 Axios: 开始创建axios实例');
    console.log('🔧 Axios: 使用的API_CONFIG:', API_CONFIG);

    // 确保baseURL使用HTTPS协议且规范格式
    let baseURL = API_CONFIG.baseURL;
    if (baseURL && baseURL.startsWith('http://')) {
      console.warn('🔧 Axios: 检测到HTTP协议，强制转换为HTTPS');
      baseURL = baseURL.replace('http://', 'https://');
    }

    // 确保baseURL末尾没有斜杠，避免URL拼接问题
    if (baseURL && baseURL.endsWith('/')) {
      console.warn('🔧 Axios: 检测到末尾斜杠，移除以避免URL拼接问题');
      baseURL = baseURL.slice(0, -1);
    }

    axiosInstance = axios.create({
      ...API_CONFIG,
      baseURL
    })

    console.log('🔧 Axios: axios实例创建完成');
    console.log('🔧 Axios: axios实例baseURL:', axiosInstance.defaults.baseURL);
    console.log('🔧 Axios: baseURL协议检查:', axiosInstance.defaults.baseURL?.startsWith('https://') ? 'HTTPS' : 'HTTP');
  }
  return axiosInstance
}

getApiInstance().interceptors.request.use(
  (config) => {
    console.log('🚀 Axios Request: 发送请求');

    // 强制确保baseURL使用HTTPS
    if (config.baseURL && config.baseURL.startsWith('http://')) {
      console.warn('🚀 Axios Request: 强制转换baseURL从HTTP到HTTPS');
      config.baseURL = config.baseURL.replace('http://', 'https://');
    }

    // 标准化URL格式：确保不以斜杠开头（避免双斜杠）
    if (config.url && config.url.startsWith('/')) {
      console.warn('🚀 Axios Request: 检测到URL以斜杠开头，移除以避免双斜杠:', config.url);
      config.url = config.url.slice(1);
    }

    console.log('🚀 Axios Request: 完整URL:', config.baseURL + config.url);
    console.log('🚀 Axios Request: 方法:', config.method?.toUpperCase());
    console.log('🚀 Axios Request: baseURL:', config.baseURL);
    console.log('🚀 Axios Request: 相对URL:', config.url);
    console.log('🚀 Axios Request: 请求头:', config.headers);
    console.log('🚀 Axios Request: 请求数据:', config.data);

    // 检查最终URL协议
    const fullUrl = config.baseURL + config.url;
    if (fullUrl.startsWith('http://')) {
      console.error('❌ 检测到HTTP请求，将导致混合内容错误:', fullUrl);
    } else if (fullUrl.startsWith('https://')) {
      console.log('✅ 请求使用HTTPS协议:', fullUrl);
    }

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

getApiInstance().interceptors.response.use(
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
  async (error) => {
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
      console.log('🔐 401错误: 检查是否需要刷新令牌')
      console.log('🔐 当前token状态:', {
        hasToken: !!authStore.token,
        hasRefreshToken: !!authStore.refreshToken,
        tokenPrefix: authStore.token ? authStore.token.substring(0, 20) + '...' : 'none',
        refreshTokenPrefix: authStore.refreshToken ? authStore.refreshToken.substring(0, 20) + '...' : 'none',
        isRetry: !!error.config._retry
      })

      // 尝试使用刷新令牌
      if (authStore.refreshToken && !error.config._retry) {
        console.log('🔄 检测到refreshToken，尝试刷新')
        error.config._retry = true
        try {
          console.log('🔄 尝试刷新令牌')
          const refreshResponse = await getApiInstance().post('/auth/refresh', {
            refresh_token: authStore.refreshToken
          })

          console.log('🔄 刷新响应:', refreshResponse.data)
          const responseData = refreshResponse.data.data || refreshResponse.data
          const { access_token } = responseData
          console.log('🔄 新的access_token:', access_token)

          if (access_token) {
            authStore.setToken(access_token)
          } else {
            console.log('❌ 刷新响应中没有access_token')
            authStore.logout()
            return Promise.reject(error)
          }

          // 重新发送原请求
          error.config.headers.Authorization = `Bearer ${access_token}`
          return getApiInstance()(error.config)
        } catch (refreshError) {
          console.log('❌ 刷新令牌失败，错误详情:', refreshError)
          console.log('❌ 可能原因：JWT密钥已更换，旧token失效')
          authStore.logout()
        }
      } else {
        if (!authStore.refreshToken) {
          console.log('🚪 没有refreshToken，可能是旧版本登录')
        } else {
          console.log('🚪 已经重试过，避免无限循环')
        }
        console.log('🚪 清除本地存储，用户需要重新登录')
        authStore.logout()
      }
    }

    return Promise.reject(error)
  }
)

// 确保配置加载的API请求函数
export const apiRequest = {
  get: async (url, config) => {
    await ensureConfigLoaded();
    return getApiInstance().get(url, config);
  },
  post: async (url, data, config) => {
    await ensureConfigLoaded();
    return getApiInstance().post(url, data, config);
  },
  put: async (url, data, config) => {
    await ensureConfigLoaded();
    return getApiInstance().put(url, data, config);
  },
  delete: async (url, config) => {
    await ensureConfigLoaded();
    return getApiInstance().delete(url, config);
  },
  patch: async (url, data, config) => {
    await ensureConfigLoaded();
    return getApiInstance().patch(url, data, config);
  }
}

// 导出api实例
export const api = {
  ...apiRequest
}
