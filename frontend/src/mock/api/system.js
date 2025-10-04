import { mockSystemLogs, mockSystemSettings } from '../data/system'
import { filterByKeyword, paginateList, simulateResponse, sortByField } from '../utils'

export const systemMockApi = {
  fetchLogs: async (params = {}) => {
    const { page = 1, pageSize = 10, level, keyword, sorter } = params

    let logs = [...mockSystemLogs]

    if (level && level !== 'ALL') {
      logs = logs.filter((item) => item.level === level)
    }

    if (keyword) {
      logs = filterByKeyword(logs, keyword, ['message', 'module', 'context.requestId'])
    }

    if (sorter?.field) {
      logs = sortByField(logs, sorter)
    }

    const pagination = paginateList(logs, { page, pageSize })
    return simulateResponse({
      items: pagination.items,
      total: pagination.total,
      page: pagination.page,
      pageSize: pagination.pageSize
    })
  },
  fetchSettings: async () => simulateResponse(mockSystemSettings),
  updateSettings: async (payload) => {
    Object.assign(mockSystemSettings, payload)
    return simulateResponse(mockSystemSettings)
  }
}
