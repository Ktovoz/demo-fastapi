import { defineStore } from 'pinia'
import { authApi } from '../api/auth'
import { createLogger } from '../utils/logger'

const logger = createLogger('AuthStore')

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    user: null,
    loading: false
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token)
  },
  actions: {
    async login(credentials) {
      this.loading = true
      try {
        // Replace with real API call when backend is ready
        const response = await authApi.login(credentials)
        this.token = response.data?.token || 'mock-token'
        this.user = response.data?.user || { name: 'Demo User', email: credentials.email }
        logger.info('User logged in')
      } catch (error) {
        logger.error('Login failed', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    logout() {
      this.token = null
      this.user = null
      logger.info('User logged out')
    }
  }
})
