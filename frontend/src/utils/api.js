import axios from 'axios'

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
    // 在发送请求之前做些什么
    console.log('API Request:', config.method?.toUpperCase(), config.url)
    return config
  },
  error => {
    // 对请求错误做些什么
    console.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 对响应数据做点什么
    console.log('API Response:', response.status, response.data)
    return response
  },
  error => {
    // 对响应错误做点什么
    console.error('Response Error:', error)

    if (error.response) {
      // 服务器返回了错误状态码
      console.error('Status:', error.response.status)
      console.error('Data:', error.response.data)
    } else if (error.request) {
      // 请求已发出但没有收到响应
      console.error('No response received:', error.request)
    } else {
      // 设置请求时发生了错误
      console.error('Request setup error:', error.message)
    }

    return Promise.reject(error)
  }
)

export { api }