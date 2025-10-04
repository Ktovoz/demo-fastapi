import { mockRoles } from '../data/roles'
import { simulateResponse } from '../utils'

let roles = [...mockRoles]

export const roleMockApi = {
  fetchRoles: async () => simulateResponse(roles),
  fetchRole: async (id) => {
    const role = roles.find((item) => item.id === Number(id))
    if (!role) {
      return Promise.reject({ status: 404, message: 'Role not found' })
    }
    return simulateResponse(role)
  },
  updateRole: async (id, payload) => {
    const index = roles.findIndex((item) => item.id === Number(id))
    if (index === -1) {
      return Promise.reject({ status: 404, message: 'Role not found' })
    }
    roles[index] = { ...roles[index], ...payload }
    return simulateResponse(roles[index])
  }
}
