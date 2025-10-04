import { defineStore } from 'pinia'
import { userApi } from '../api/user'
import { createLogger } from '../utils/logger'

const logger = createLogger('UserStore')

export const useUserStore = defineStore('user', {
  state: () => ({
    list: [],
    total: 0,
    filters: {},
    loading: false,
    selectedUser: null
  }),
  actions: {
    async fetchUsers(params = {}) {
      this.loading = true
      try {
        const response = await userApi.fetchUsers(params)
        this.list = response.data?.items || []
        this.total = response.data?.total || 0
      } catch (error) {
        logger.error('Failed to fetch users', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchUserDetail(id) {
      try {
        const response = await userApi.fetchUser(id)
        this.selectedUser = response.data
      } catch (error) {
        logger.error('Failed to fetch user detail', error)
        throw error
      }
    },
    setFilters(filters) {
      this.filters = { ...filters }
    }
  }
})
