import { apiRequest } from '../utils/api'
import { isMockEnabled, mockApi } from '../mock'

export const roleApi = {
  fetchRoles(params) {
    if (isMockEnabled) {
      return mockApi.roles.fetchRoles(params)
    }
    return apiRequest.get('/roles', { params })
  },
  fetchRole(id) {
    if (isMockEnabled) {
      return mockApi.roles.fetchRole(id)
    }
    return apiRequest.get(`/roles/${id}`)
  },
  updateRole(id, payload) {
    if (isMockEnabled) {
      return mockApi.roles.updateRole(id, payload)
    }
    return apiRequest.put(`/roles/${id}`, payload)
  }
}
