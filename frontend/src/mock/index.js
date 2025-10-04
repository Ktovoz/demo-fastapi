import { authMockApi } from './api/auth'
import { userMockApi } from './api/users'
import { roleMockApi } from './api/roles'
import { dashboardMockApi } from './api/dashboard'
import { systemMockApi } from './api/system'
import { adminMockApi } from './api/admin'

const mockFlagRaw = import.meta.env.VITE_USE_MOCK
const normalizedFlag = typeof mockFlagRaw === 'string'
  ? mockFlagRaw
  : mockFlagRaw == null
    ? ''
    : String(mockFlagRaw)

const flag = normalizedFlag.trim().toLowerCase()
export const isMockEnabled = ['true', '1', 'yes', 'on'].includes(flag)

if (import.meta.env.DEV) {
  const mode = isMockEnabled ? 'mock' : 'real'
  const flagLabel = flag || 'unset'
  console.info(`[mock] API mock mode: ${mode} (VITE_USE_MOCK=${flagLabel})`);
}

export const mockApi = {
  auth: authMockApi,
  users: userMockApi,
  roles: roleMockApi,
  dashboard: dashboardMockApi,
  system: systemMockApi,
  admin: adminMockApi
}

export const callMock = (namespace, method, ...args) => {
  const module = mockApi[namespace]
  if (!module) {
    throw new Error(`Mock namespace "${namespace}" not found`)
  }
  const handler = module[method]
  if (typeof handler !== 'function') {
    throw new Error(`Mock method "${method}" not found in namespace "${namespace}"`)
  }
  return handler(...args)
}

