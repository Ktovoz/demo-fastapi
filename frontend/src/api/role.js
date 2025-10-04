import { apiRequest } from '../utils/api'

export const roleApi = {
  fetchRoles(params) {
    return apiRequest.get('/roles', { params })
  },
  fetchRole(id) {
    return apiRequest.get(`/roles/${id}`)
  },
  updateRole(id, payload) {
    return apiRequest.put(`/roles/${id}`, payload)
  }
}
