import { mockUsers } from '../data/users'
import { filterByKeyword, paginateList, simulateResponse, sortByField } from '../utils'

let users = [...mockUsers]

const roleLabelMap = {
  admin: '管理员',
  manager: '经理',
  support: '客服',
  user: '普通用户'
}

const applyFilters = (collection, filters = {}) => {
  let result = [...collection]

  if (filters.keyword) {
    result = filterByKeyword(result, filters.keyword, ['name', 'email', 'department'])
  }

  if (filters.status && filters.status !== 'all') {
    result = result.filter((item) => item.status === filters.status)
  }

  if (filters.role && filters.role !== 'all') {
    result = result.filter((item) => item.role === filters.role)
  }

  if (filters.tags?.length) {
    result = result.filter((item) => item.tags.some((tag) => filters.tags.includes(tag)))
  }

  if (filters.department?.length) {
    const departments = Array.isArray(filters.department) ? filters.department : [filters.department]
    result = result.filter((item) => departments.includes(item.department))
  }

  if (filters.sorter) {
    result = sortByField(result, filters.sorter)
  }

  return result
}

export const userMockApi = {
  fetchUsers: async (params = {}) => {
    const { page = 1, pageSize = 10, sorter, ...filters } = params
    const filtered = applyFilters(users, { ...filters, sorter })
    const pagination = paginateList(filtered, { page, pageSize })

    return simulateResponse({
      items: pagination.items,
      total: pagination.total,
      page: pagination.page,
      pageSize: pagination.pageSize
    })
  },

  fetchUser: async (id) => {
    const user = users.find((item) => item.id === Number(id))
    if (!user) {
      return Promise.reject({ status: 404, message: 'User not found' })
    }
    return simulateResponse(user)
  },

  createUser: async (payload) => {
    const id = users.length ? Math.max(...users.map((item) => item.id)) + 1 : 1
    const role = payload.role || 'user'
    const newUser = {
      id,
      name: payload.name,
      email: payload.email,
      role,
      roleName: roleLabelMap[role] || payload.roleName || 'User',
      status: payload.status || 'active',
      createdAt: new Date().toISOString().slice(0, 10),
      lastLogin: null,
      department: payload.department || 'Operations',
      phone: payload.phone || '',
      tags: payload.tags || [],
      permissions: payload.permissions || ['users:view']
    }
    users.unshift(newUser)
    return simulateResponse(newUser)
  },

  updateUser: async (id, payload) => {
    const index = users.findIndex((item) => item.id === Number(id))
    if (index === -1) {
      return Promise.reject({ status: 404, message: 'User not found' })
    }
    const merged = { ...users[index], ...payload }
    const role = merged.role || 'user'
    merged.role = role
    merged.roleName = roleLabelMap[role] || merged.roleName || 'User'
    users[index] = merged
    return simulateResponse(users[index])
  },

  toggleUserStatus: async (id) => {
    const index = users.findIndex((item) => item.id === Number(id))
    if (index === -1) {
      return Promise.reject({ status: 404, message: 'User not found' })
    }
    const current = users[index]
    const nextStatus = current.status === 'active' ? 'inactive' : 'active'
    users[index] = { ...current, status: nextStatus }
    return simulateResponse(users[index])
  },

  deleteUsers: async (ids = []) => {
    const idSet = new Set(ids.map((value) => Number(value)))
    users = users.filter((item) => !idSet.has(item.id))
    return simulateResponse({ success: true, remaining: users.length })
  }
}
