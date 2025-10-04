import { defineStore } from 'pinia'
import { adminApi } from '../api/admin'
import { createLogger } from '../utils/logger'

const logger = createLogger('AdminStore')

const defaultTaskFilters = () => ({
  keyword: '',
  status: 'all',
  priority: 'all',
  tags: []
})

const defaultTaskPagination = () => ({
  page: 1,
  pageSize: 6
})

export const useAdminStore = defineStore('admin', {
  state: () => ({
    overview: null,
    overviewLoading: false,
    alerts: [],
    alertsLoading: false,
    tasks: [],
    taskTotal: 0,
    taskLoading: false,
    taskFilters: defaultTaskFilters(),
    taskPagination: defaultTaskPagination(),
    taskSorter: null,
    timeline: [],
    timelineLoading: false
  }),
  actions: {
    async fetchOverview() {
      this.overviewLoading = true
      try {
        const response = await adminApi.fetchOverview()
        this.overview = response.data
        logger.info('Loaded admin overview')
      } catch (error) {
        logger.error('Failed to load admin overview', error)
        throw error
      } finally {
        this.overviewLoading = false
      }
    },

    async fetchAlerts() {
      this.alertsLoading = true
      try {
        const response = await adminApi.fetchAlerts()
        this.alerts = response.data
        logger.info('Loaded admin alerts', { total: this.alerts.length })
      } catch (error) {
        logger.error('Failed to load alerts', error)
        throw error
      } finally {
        this.alertsLoading = false
      }
    },

    async acknowledgeAlert(id) {
      try {
        const response = await adminApi.acknowledgeAlert(id)
        this.alerts = this.alerts.map((item) =>
          item.id === id ? response.data : item
        )
        logger.info('Alert acknowledged', { id })
      } catch (error) {
        logger.error('Failed to acknowledge alert', { id, error })
        throw error
      }
    },

    async fetchTasks(extra = {}) {
      this.taskLoading = true
      try {
        const params = {
          ...this.taskFilters,
          ...this.taskPagination,
          sorter: this.taskSorter,
          ...extra
        }
        const response = await adminApi.fetchTasks(params)
        this.tasks = response.data.items
        this.taskTotal = response.data.total
        this.taskPagination.page = response.data.page
        this.taskPagination.pageSize = response.data.pageSize
        logger.info('Loaded admin tasks', { total: this.taskTotal })
      } catch (error) {
        logger.error('Failed to load tasks', error)
        throw error
      } finally {
        this.taskLoading = false
      }
    },

    async updateTask(id, payload) {
      try {
        const response = await adminApi.updateTask(id, payload)
        this.tasks = this.tasks.map((item) =>
          item.id === id ? response.data : item
        )
        logger.info('Updated task', { id })
        return response.data
      } catch (error) {
        logger.error('Failed to update task', { id, error })
        throw error
      }
    },

    async createTask(payload) {
      try {
        const response = await adminApi.createTask(payload)
        this.tasks = [response.data, ...this.tasks]
        if (this.tasks.length > this.taskPagination.pageSize) {
          this.tasks.pop()
        }
        logger.info('Created new task', { id: response.data.id })
        return response.data
      } catch (error) {
        logger.error('Failed to create task', error)
        throw error
      }
    },

    async fetchTimeline() {
      this.timelineLoading = true
      try {
        const response = await adminApi.fetchAuditTimeline()
        this.timeline = response.data
        logger.info('Loaded audit timeline', { total: this.timeline.length })
      } catch (error) {
        logger.error('Failed to load timeline', error)
        throw error
      } finally {
        this.timelineLoading = false
      }
    },

    setTaskFilters(filters) {
      this.taskFilters = { ...this.taskFilters, ...filters }
    },

    resetTaskFilters() {
      this.taskFilters = defaultTaskFilters()
    },

    setTaskPagination(pagination) {
      this.taskPagination = { ...this.taskPagination, ...pagination }
    },

    setTaskSorter(sorter) {
      this.taskSorter = sorter
    }
  }
})
