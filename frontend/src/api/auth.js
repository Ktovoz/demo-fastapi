import { apiRequest } from '../utils/api'

export const authApi = {
  login(payload) {
    return apiRequest.post('/auth/login', payload)
  },
  register(payload) {
    return apiRequest.post('/auth/register', payload)
  },
  requestPasswordReset(payload) {
    return apiRequest.post('/auth/forgot-password', payload)
  }
}
