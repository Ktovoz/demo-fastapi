import { apiRequest } from '../utils/api'
import { isMockEnabled, mockApi } from '../mock'

export const authApi = {
  login(payload) {
    if (isMockEnabled) {
      return mockApi.auth.login(payload)
    }
    return apiRequest.post('/auth/login', payload)
  },
  register(payload) {
    if (isMockEnabled) {
      return mockApi.auth.register(payload)
    }
    return apiRequest.post('/auth/register', payload)
  },
  requestPasswordReset(payload) {
    if (isMockEnabled) {
      return mockApi.auth.requestPasswordReset(payload)
    }
    return apiRequest.post('/auth/forgot-password', payload)
  }
}
