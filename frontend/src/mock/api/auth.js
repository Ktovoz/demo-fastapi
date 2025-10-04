import { mockAccounts } from '../data/auth'
import { simulateResponse } from '../utils'

const createToken = (id) => `mock-token-${id}-${Date.now()}`

export const authMockApi = {
  login: async ({ email, password, remember = false }) => {
    const account = mockAccounts.find((item) => item.email === email)
    if (!account || account.password !== password) {
      return Promise.reject({
        status: 401,
        message: 'Invalid email or password'
      })
    }

    const token = createToken(account.id)
    const expiresIn = remember ? 60 * 24 * 7 : 60 * 8

    return simulateResponse({
      token,
      user: {
        id: account.id,
        name: account.name,
        email: account.email,
        role: account.role,
        permissions: account.permissions,
        lastLogin: account.lastLogin
      },
      expiresIn
    })
  },
  register: async (payload) => {
    const exists = mockAccounts.some((item) => item.email === payload.email)
    if (exists) {
      return Promise.reject({
        status: 409,
        message: 'Email already registered'
      })
    }

    const newAccount = {
      ...payload,
      id: mockAccounts.length + 1,
      role: 'user',
      permissions: ['dashboard:view'],
      lastLogin: new Date().toISOString()
    }
    mockAccounts.push(newAccount)

    return simulateResponse({
      id: newAccount.id,
      email: newAccount.email,
      name: newAccount.name
    })
  },
  requestPasswordReset: async ({ email }) => {
    const account = mockAccounts.find((item) => item.email === email)
    if (!account) {
      return Promise.reject({
        status: 404,
        message: 'User not found'
      })
    }

    return simulateResponse({ success: true, email })
  }
}
