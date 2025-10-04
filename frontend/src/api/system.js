import { apiRequest } from '../utils/api'

export const systemApi = {
  fetchLogs(params) {
    return apiRequest.get('/system/logs', { params })
  },
  fetchSettings() {
    return apiRequest.get('/system/settings')
  },
  updateSettings(payload) {
    return apiRequest.put('/system/settings', payload)
  }
}
