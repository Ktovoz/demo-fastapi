import {
  adminOverviewCards,
  adminTrafficTrend,
  adminServiceHealth,
  adminAlertFeed,
  adminTaskBoard,
  adminAuditTimeline,
  adminTeamShifts
} from '../data/admin'
import { filterByKeyword, paginateList, simulateResponse, sortByField } from '../utils'

let alerts = adminAlertFeed.map((item) => ({ ...item }))
let tasks = adminTaskBoard.map((item) => ({ ...item }))

const filterTasks = (collection, filters = {}) => {
  let result = [...collection]

  if (filters.keyword) {
    result = filterByKeyword(result, filters.keyword, ['title', 'assignee', 'tags'])
  }

  if (filters.status && filters.status !== 'all') {
    result = result.filter((item) => item.status === filters.status)
  }

  if (filters.priority && filters.priority !== 'all') {
    result = result.filter((item) => item.priority === filters.priority)
  }

  if (filters.tags?.length) {
    const tagSet = new Set(filters.tags)
    result = result.filter((item) => item.tags.some((tag) => tagSet.has(tag)))
  }

  if (filters.sorter) {
    result = sortByField(result, filters.sorter)
  }

  return result
}

export const adminMockApi = {
  async fetchOverview () {
    return simulateResponse({
      cards: adminOverviewCards,
      trend: adminTrafficTrend,
      services: adminServiceHealth,
      shifts: adminTeamShifts
    }, { delay: 260 })
  },

  async fetchAlerts () {
    return simulateResponse(alerts, { delay: 200 })
  },

  async acknowledgeAlert (id) {
    alerts = alerts.map((item) =>
      item.id === id ? { ...item, acknowledged: true } : item
    )
    const target = alerts.find((item) => item.id === id)
    if (!target) {
      return Promise.reject({ status: 404, message: 'Alert not found' })
    }
    return simulateResponse(target)
  },

  async fetchTasks (params = {}) {
    const { page = 1, pageSize = 8, sorter, ...filters } = params
    const filtered = filterTasks(tasks, { ...filters, sorter })
    const pagination = paginateList(filtered, { page, pageSize })

    return simulateResponse({
      items: pagination.items,
      total: pagination.total,
      page: pagination.page,
      pageSize: pagination.pageSize
    }, { delay: 180 })
  },

  async updateTask (id, payload) {
    const index = tasks.findIndex((item) => item.id === id)
    if (index === -1) {
      return Promise.reject({ status: 404, message: 'Task not found' })
    }
    tasks[index] = { ...tasks[index], ...payload }
    return simulateResponse(tasks[index], { delay: 150 })
  },

  async createTask (payload) {
    const id = `TASK-${Math.floor(Math.random() * 10000)}`
    const task = {
      id,
      title: payload.title || '新建任务',
      assignee: payload.assignee || '待分配',
      avatarColor: payload.avatarColor || '#64748b',
      due: payload.due || new Date().toISOString().slice(0, 10),
      priority: payload.priority || 'low',
      status: payload.status || 'todo',
      tags: payload.tags || []
    }
    tasks.unshift(task)
    return simulateResponse(task, { delay: 150 })
  },

  async fetchAuditTimeline () {
    return simulateResponse(adminAuditTimeline, { delay: 160 })
  }
}
