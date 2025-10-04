import { apiRequest } from '../utils/api'
import { isMockEnabled, mockApi } from '../mock'

export const systemApi = {
  fetchLogs(params) {
    if (isMockEnabled) {
      return mockApi.system.fetchLogs(params)
    }
    return apiRequest.get('/system/logs', { params })
  },
  fetchSettings() {
    if (isMockEnabled) {
      return mockApi.system.fetchSettings()
    }
    return apiRequest.get('/system/settings')
  },
  updateSettings(payload) {
    if (isMockEnabled) {
      return mockApi.system.updateSettings(payload)
    }
    return apiRequest.put('/system/settings', payload)
  }
}
