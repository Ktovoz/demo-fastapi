import { defineStore } from "pinia"
import { systemApi } from "../api/system"
import { createLogger } from "../utils/logger"
import { ensureConfigLoaded } from "../config/api"

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
    ],
    systemStatus: null,
    resetLoading: false,
    schedulerStatus: null
  }),
  actions: {
    setMenuCollapsed(value) {
      this.menuCollapsed = Boolean(value)
    },

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
        await ensureConfigLoaded()
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
        await ensureConfigLoaded()
        const params = {
          ...this.logFilters,
          ...this.logPagination,
          sorter: this.logSorter,
          ...extra
        }
        const response = await systemApi.fetchLogs(params)
        logger.debug("Logs API response:", response)
        // 修复数据访问路径：后端返回的是 { success: true, data: { items: [...], total: 60, page: 1, pageSize: 10 } }
        const responseData = response.data.data || response.data
        this.logs = responseData.items || []
        this.logTotal = responseData.total || 0
        this.logPagination.page = responseData.page || 1
        this.logPagination.pageSize = responseData.pageSize || 10
        logger.info("Loaded system logs", { total: this.logTotal, itemsCount: this.logs.length })
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
        logger.debug("Log summary API response:", response)
        // 修复数据访问路径：后端返回的是 { success: true, data: { severity: {...}, recent: [...] } }
        this.logSummary = response.data.data || response.data
        logger.info("Loaded log summary", { total: this.logSummary?.total || 0 })
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
    },

    async fetchSystemStatus() {
      try {
        await ensureConfigLoaded()
        const response = await systemApi.getSystemStatus()
        this.systemStatus = response.data
        logger.info("获取系统状态成功")
        return response.data
      } catch (error) {
        logger.error("获取系统状态失败", error)
        throw error
      }
    },

    async resetSystem() {
      this.resetLoading = true
      try {
        const response = await systemApi.resetSystem()
        logger.info("系统重置成功")
        return response.data
      } catch (error) {
        logger.error("系统重置失败", error)
        throw error
      } finally {
        this.resetLoading = false
      }
    },

    async fetchSchedulerStatus() {
      try {
        const response = await systemApi.getSchedulerStatus()
        this.schedulerStatus = response.data
        logger.info("获取调度器状态成功")
        return response.data
      } catch (error) {
        logger.error("获取调度器状态失败", error)
        throw error
      }
    },

    async fixAdminSuperuser() {
      try {
        const response = await systemApi.fixAdminSuperuser()
        logger.info("修复admin权限成功", response.data)
        return response.data
      } catch (error) {
        logger.error("修复admin权限失败", error)
        throw error
      }
    }
  }
})
