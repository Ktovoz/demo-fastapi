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
        logger.debug("Fetching users with params:", params)
        const response = await userApi.fetchUsers(params)
        logger.debug("Users API response:", response)

        // 适配后端API响应结构 (BaseResponse/PaginatedResponse包装)
        if (response.data && response.data.data) {
          // 后端API返回的结构: { data: { data: { items, total, page, pageSize } } }
          const responseData = response.data.data
          this.list = responseData.items || []
          this.total = responseData.total || 0
          this.pagination.page = responseData.page || 1
          this.pagination.pageSize = responseData.pageSize || 10
          logger.info("Loaded user list from backend API", { total: this.total })
        } else if (response.data && (response.data.items || Array.isArray(response.data))) {
          // Mock数据或直接返回的结构: { data: { items, total, page, pageSize } } 或 { data: [users] }
          if (Array.isArray(response.data)) {
            this.list = response.data
            this.total = response.data.length
            this.pagination.page = 1
            this.pagination.pageSize = 10
          } else {
            this.list = response.data.items || []
            this.total = response.data.total || 0
            this.pagination.page = response.data.page || 1
            this.pagination.pageSize = response.data.pageSize || 10
          }
          logger.info("Loaded user list from mock/direct API", { total: this.total })
        } else {
          logger.warn("Unexpected API response structure:", response)
          this.list = []
          this.total = 0
        }
      } catch (error) {
        logger.error("Failed to fetch users", error)
        this.list = []
        this.total = 0
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchUserDetail(id) {
      try {
        const response = await userApi.fetchUser(id)
        logger.debug("User detail API response:", response)

        // 适配后端API响应结构
        const userData = response.data?.data || response.data
        this.currentUser = userData
        logger.info("Loaded user detail", { id, name: userData?.name })
        return userData
      } catch (error) {
        logger.error("Failed to fetch user detail", { id, error })
        throw error
      }
    },

    async updateUser(id, payload) {
      try {
        const response = await userApi.updateUser(id, payload)
        logger.debug("Update user API response:", response)

        // 适配后端API响应结构
        const userData = response.data?.data || response.data
        this.currentUser = userData
        this.list = this.list.map((item) => (item.id === userData.id ? userData : item))
        logger.info("User updated", { id, name: userData?.name })
        return userData
      } catch (error) {
        logger.error("Failed to update user", { id, error })
        throw error
      }
    },

    async toggleUserStatus(id) {
      try {
        const response = await userApi.toggleUserStatus(id)
        logger.debug("Toggle user status API response:", response)

        // 适配后端API响应结构
        const userData = response.data?.data || response.data
        this.list = this.list.map((item) => (item.id === userData.id ? userData : item))
        if (this.currentUser?.id === userData.id) {
          this.currentUser = userData
        }
        logger.info("User status toggled", { id, status: userData.status })
        return userData
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
        logger.debug("Create user API response:", response)

        // 适配后端API响应结构
        const userData = response.data?.data || response.data
        logger.info("User created", { id: userData.id, name: userData.name })
        await this.fetchUsers({ page: 1 })
        return userData
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
