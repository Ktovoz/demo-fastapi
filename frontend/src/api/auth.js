import { apiRequest } from '../utils/api'
import { isMockEnabled, mockApi } from '../mock'

export const authApi = {
  login(payload) {
    console.log('🔐 Auth API: 开始登录请求');
    console.log('🔐 Auth API: 是否使用Mock:', isMockEnabled);
    console.log('🔐 Auth API: 登录载荷:', payload);

    if (isMockEnabled) {
      console.log('🔐 Auth API: 使用Mock数据登录');
      return mockApi.auth.login(payload)
    }

    console.log('🔐 Auth API: 使用真实API登录');
    console.log('🔐 Auth API: 请求路径: /auth/login-json');
    // 使用 JSON 格式的登录接口，支持 email 字段
    return apiRequest.post('auth/login-json', payload)
  },
  register(payload) {
    if (isMockEnabled) {
      return mockApi.auth.register(payload)
    }
    return apiRequest.post('auth/register', payload)
  },
  requestPasswordReset(payload) {
    if (isMockEnabled) {
      return mockApi.auth.requestPasswordReset(payload)
    }
    return apiRequest.post('auth/forgot-password', payload)
  }
}
