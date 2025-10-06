import { apiRequest } from '../utils/api'
import { isMockEnabled, mockApi } from '../mock'

export const systemApi = {
  fetchLogs(params) {
    if (isMockEnabled) {
      return mockApi.system.fetchLogs(params)
    }
    return apiRequest.get('system/logs', { params })
  },
  fetchLogSummary() {
    if (isMockEnabled) {
      return mockApi.system.fetchLogSummary()
    }
    return apiRequest.get('system/logs/summary')
  },
  fetchSettings() {
    if (isMockEnabled) {
      return mockApi.system.fetchSettings()
    }
    return apiRequest.get('system/settings')
  },
  updateSettings(payload) {
    if (isMockEnabled) {
      return mockApi.system.updateSettings(payload)
    }
    return apiRequest.put('system/settings', payload)
  },
  getSystemStatus() {
    if (isMockEnabled) {
      return mockApi.system.getSystemStatus()
    }
    return apiRequest.get('system/system/status')
  },
  resetSystem() {
    if (isMockEnabled) {
      return mockApi.system.resetSystem()
    }
    return apiRequest.post('system/system/reset')
  },
  getSchedulerStatus() {
    if (isMockEnabled) {
      return mockApi.system.getSchedulerStatus()
    }
    return apiRequest.get('scheduler/status')
  },
  fixAdminSuperuser() {
    if (isMockEnabled) {
      return Promise.resolve({
        data: {
          success: true,
          message: "admin用户权限修复成功（模拟）",
          data: {
            user_id: 1,
            username: "admin",
            email: "admin@example.com",
            is_superuser: true
          }
        }
      })
    }
    return apiRequest.post('system/system/fix-admin')
  }
}
