import { apiRequest } from '../utils/api'
import { isMockEnabled, mockApi } from '../mock'

export const adminApi = {
  fetchOverview() {
    if (isMockEnabled) {
      return mockApi.admin.fetchOverview()
    }
    return apiRequest.get('/admin/overview')
  },
  fetchAlerts() {
    if (isMockEnabled) {
      return mockApi.admin.fetchAlerts()
    }
    return apiRequest.get('/admin/alerts')
  },
  acknowledgeAlert(id) {
    if (isMockEnabled) {
      return mockApi.admin.acknowledgeAlert(id)
    }
    return apiRequest.post(`/admin/alerts/${id}/acknowledge`)
  },
  fetchTasks(params) {
    if (isMockEnabled) {
      return mockApi.admin.fetchTasks(params)
    }
    return apiRequest.get('/admin/tasks', { params })
  },
  updateTask(id, payload) {
    if (isMockEnabled) {
      return mockApi.admin.updateTask(id, payload)
    }
    return apiRequest.patch(`/admin/tasks/${id}`, payload)
  },
  createTask(payload) {
    if (isMockEnabled) {
      return mockApi.admin.createTask(payload)
    }
    return apiRequest.post('/admin/tasks', payload)
  },
  fetchAuditTimeline() {
    if (isMockEnabled) {
      return mockApi.admin.fetchAuditTimeline()
    }
    return apiRequest.get('/admin/audit-timeline')
  }
}
