import { authMockApi } from './api/auth'
import { userMockApi } from './api/users'
import { roleMockApi } from './api/roles'
import { dashboardMockApi } from './api/dashboard'
import { systemMockApi } from './api/system'

const flag = (import.meta.env.VITE_USE_MOCK ?? (import.meta.env.DEV ? 'true' : 'false')).toString().toLowerCase()

export const isMockEnabled = flag !== 'false' && flag !== '0'

export const mockApi = {
  auth: authMockApi,
  users: userMockApi,
  roles: roleMockApi,
  dashboard: dashboardMockApi,
  system: systemMockApi
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
