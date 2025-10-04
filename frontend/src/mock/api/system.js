import { mockSystemLogs, mockSystemSettings } from '../data/system'
import { filterByKeyword, paginateList, simulateResponse, sortByField } from '../utils'

const computeLogSummary = () => {
  const severity = {
    INFO: 0,
    WARN: 0,
    ERROR: 0,
    DEBUG: 0
  }

  const moduleCount = new Map()

  mockSystemLogs.forEach((log) => {
    const level = log.level?.toUpperCase?.() || 'INFO'
    if (severity[level] != null) {
      severity[level] += 1
    }
    moduleCount.set(log.module, (moduleCount.get(log.module) || 0) + 1)
  })

  const topModules = Array.from(moduleCount.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([module, total]) => ({ module, total }))

  const recent = [...mockSystemLogs]
    .sort((a, b) => new Date(b.time) - new Date(a.time))
    .slice(0, 6)

  const total = mockSystemLogs.length
  const errorRatio = total ? Number(((severity.ERROR + severity.WARN) / total * 100).toFixed(1)) : 0

  return {
    severity,
    topModules,
    recent,
    total,
    errorRatio
  }
}

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
  fetchLogSummary: async () => {
    return simulateResponse(computeLogSummary())
  },
  fetchSettings: async () => simulateResponse(mockSystemSettings),
  updateSettings: async (payload) => {
    Object.assign(mockSystemSettings, payload)
    return simulateResponse(mockSystemSettings)
  }
}
