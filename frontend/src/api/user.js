import { apiRequest } from '../utils/api'

export const userApi = {
  fetchUsers(params) {
    return apiRequest.get('/users', { params })
  },
  fetchUser(id) {
    return apiRequest.get(`/users/${id}`)
  },
  createUser(payload) {
    return apiRequest.post('/users', payload)
  },
  updateUser(id, payload) {
    return apiRequest.put(`/users/${id}`, payload)
  },
  deleteUser(id) {
    return apiRequest.delete(`/users/${id}`)
  }
}
