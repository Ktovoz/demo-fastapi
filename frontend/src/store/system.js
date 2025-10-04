import { defineStore } from 'pinia'
import { systemApi } from '../api/system'
import { createLogger } from '../utils/logger'

const logger = createLogger('SystemStore')

export const useSystemStore = defineStore('system', {
  state: () => ({
    settings: null,
    logs: [],
    loading: false
  }),
  actions: {
    async fetchSettings() {
      this.loading = true
      try {
        const response = await systemApi.fetchSettings()
        this.settings = response.data
      } catch (error) {
        logger.error('Failed to fetch settings', error)
      } finally {
        this.loading = false
      }
    },
    async fetchLogs(params = {}) {
      this.loading = true
      try {
        const response = await systemApi.fetchLogs(params)
        this.logs = response.data?.items || []
      } catch (error) {
        logger.error('Failed to fetch logs', error)
      } finally {
        this.loading = false
      }
    }
  }
})
