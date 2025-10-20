import { apiRequest } from "../utils/api"
import { isMockEnabled, mockApi } from "../mock"

export const userApi = {
  fetchUsers(params) {
    if (isMockEnabled) {
      console.log("Using mock data for users")
      return mockApi.users.fetchUsers(params)
    }
    console.log("Fetching users from API with params:", params)
    return apiRequest.get("users", { params })
  },
  fetchUser(id) {
    if (isMockEnabled) {
      return mockApi.users.fetchUser(id)
    }
    return apiRequest.get(`users/${id}`)
  },
  createUser(payload) {
    if (isMockEnabled) {
      return mockApi.users.createUser(payload)
    }
    return apiRequest.post("users", payload)
  },
  updateUser(id, payload) {
    if (isMockEnabled) {
      return mockApi.users.updateUser(id, payload)
    }
    return apiRequest.put(`users/${id}`, payload)
  },
  deleteUser(id) {
    if (isMockEnabled) {
      return mockApi.users.deleteUsers([id])
    }
    return apiRequest.delete(`users/${id}`)
  },
  deleteUsers(ids = []) {
    if (isMockEnabled) {
      return mockApi.users.deleteUsers(ids)
    }
    return apiRequest.post("users/bulk-delete", { ids })
  },
  toggleUserStatus(id) {
    if (isMockEnabled) {
      return mockApi.users.toggleUserStatus(id)
    }
    return apiRequest.patch(`users/${id}/status`)
  }
}
