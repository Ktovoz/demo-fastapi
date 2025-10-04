import { defineStore } from "pinia"
import { userApi } from "../api/user"
import { createLogger } from "../utils/logger"

const logger = createLogger("UserStore")

const defaultFilters = () => ({
  keyword: "",
  status: "all",
  role: "all",
  tags: [],
  department: []
})

const defaultPagination = () => ({
  page: 1,
  pageSize: 10
})

export const useUserStore = defineStore("user", {
  state: () => ({
    list: [],
    total: 0,
    loading: false,
    filters: defaultFilters(),
    pagination: defaultPagination(),
    sorter: null,
    selectedRowKeys: [],
    currentUser: null
  }),
  actions: {
    async fetchUsers(extra = {}) {
      this.loading = true
      try {
        const params = {
          ...this.filters,
          ...this.pagination,
          sorter: this.sorter,
          ...extra
        }
        const response = await userApi.fetchUsers(params)
        this.list = response.data.items
        this.total = response.data.total
        this.pagination.page = response.data.page
        this.pagination.pageSize = response.data.pageSize
        logger.info("Loaded user list", { total: this.total })
      } catch (error) {
        logger.error("Failed to fetch users", error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchUserDetail(id) {
      try {
        const response = await userApi.fetchUser(id)
        this.currentUser = response.data
        return response.data
      } catch (error) {
        logger.error("Failed to fetch user detail", { id, error })
        throw error
      }
    },

    async updateUser(id, payload) {
      try {
        const response = await userApi.updateUser(id, payload)
        this.currentUser = response.data
        this.list = this.list.map((item) => (item.id === response.data.id ? response.data : item))
        logger.info("User updated", { id })
        return response.data
      } catch (error) {
        logger.error("Failed to update user", { id, error })
        throw error
      }
    },

    async toggleUserStatus(id) {
      try {
        const response = await userApi.toggleUserStatus(id)
        this.list = this.list.map((item) => (item.id === response.data.id ? response.data : item))
        if (this.currentUser?.id === response.data.id) {
          this.currentUser = response.data
        }
        logger.info("User status toggled", { id, status: response.data.status })
        return response.data
      } catch (error) {
        logger.error("Failed to toggle user status", { id, error })
        throw error
      }
    },

    async deleteUsers(ids = []) {
      try {
        await userApi.deleteUsers(ids)
        this.selectedRowKeys = []
        logger.info("Users deleted", { ids })
        await this.fetchUsers({ page: 1 })
      } catch (error) {
        logger.error("Failed to delete users", { ids, error })
        throw error
      }
    },

    async createUser(payload) {
      try {
        const response = await userApi.createUser(payload)
        logger.info("User created", { id: response.data.id })
        await this.fetchUsers({ page: 1 })
        return response.data
      } catch (error) {
        logger.error("Failed to create user", error)
        throw error
      }
    },

    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
    },

    resetFilters() {
      this.filters = defaultFilters()
    },

    setPagination(pagination) {
      this.pagination = { ...this.pagination, ...pagination }
    },

    setSorter(sorter) {
      this.sorter = sorter
    },

    setSelectedRowKeys(keys) {
      this.selectedRowKeys = keys
    }
  }
})
