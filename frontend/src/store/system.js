import { defineStore } from "pinia"
import { systemApi } from "../api/system"
import { createLogger } from "../utils/logger"

const logger = createLogger("SystemStore")

const defaultLogFilters = () => ({
  keyword: "",
  level: "ALL"
})

const defaultLogPagination = () => ({
  page: 1,
  pageSize: 10
})

export const useSystemStore = defineStore("system", {
  state: () => ({
    settings: null,
    logs: [],
    logTotal: 0,
    logLoading: false,
    logSummary: null,
    logSummaryLoading: false,
    logFilters: defaultLogFilters(),
    logSorter: null,
    logPagination: defaultLogPagination(),
    menuCollapsed: false,
    theme: "light",
    notifications: [
      { id: 1, title: "Deployment successful", read: false, time: "2025-10-04 09:20" },
      { id: 2, title: "3 security alerts", read: false, time: "2025-10-04 08:45" },
      { id: 3, title: "Weekly report available", read: true, time: "2025-10-03 18:00" }
    ]
  }),
  actions: {
    toggleMenu() {
      this.menuCollapsed = !this.menuCollapsed
    },

    setTheme(theme) {
      this.theme = theme
    },

    markNotificationRead(id) {
      this.notifications = this.notifications.map((item) =>
        item.id === id ? { ...item, read: true } : item
      )
    },

    clearNotifications() {
      this.notifications = []
    },

    async fetchSettings() {
      try {
        const response = await systemApi.fetchSettings()
        this.settings = response.data
        logger.info("Loaded system settings")
      } catch (error) {
        logger.error("Failed to load settings", error)
        throw error
      }
    },

    async updateSettings(payload) {
      try {
        const response = await systemApi.updateSettings(payload)
        this.settings = response.data
        logger.info("Updated system settings")
        return response.data
      } catch (error) {
        logger.error("Failed to update settings", error)
        throw error
      }
    },

    async fetchLogs(extra = {}) {
      this.logLoading = true
      try {
        const params = {
          ...this.logFilters,
          ...this.logPagination,
          sorter: this.logSorter,
          ...extra
        }
        const response = await systemApi.fetchLogs(params)
        this.logs = response.data.items
        this.logTotal = response.data.total
        this.logPagination.page = response.data.page
        this.logPagination.pageSize = response.data.pageSize
        logger.info("Loaded system logs", { total: this.logTotal })
      } catch (error) {
        logger.error("Failed to load logs", error)
        throw error
      } finally {
        this.logLoading = false
      }
    },

    async fetchLogSummary() {
      this.logSummaryLoading = true
      try {
        const response = await systemApi.fetchLogSummary()
        this.logSummary = response.data
        logger.info("Loaded log summary")
      } catch (error) {
        logger.error("Failed to load log summary", error)
        throw error
      } finally {
        this.logSummaryLoading = false
      }
    },

    setLogFilters(filters) {
      this.logFilters = { ...this.logFilters, ...filters }
    },

    resetLogFilters() {
      this.logFilters = defaultLogFilters()
    },

    setLogPagination(pagination) {
      this.logPagination = { ...this.logPagination, ...pagination }
    },

    setLogSorter(sorter) {
      this.logSorter = sorter
    }
  }
})
