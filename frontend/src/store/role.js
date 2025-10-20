import { defineStore } from "pinia"
import { roleApi } from "../api/role"
import { createLogger } from "../utils/logger"
import { ensureConfigLoaded } from "../config/api"

const logger = createLogger("RoleStore")

export const useRoleStore = defineStore("role", {
  state: () => ({
    list: [],
    loading: false,
    currentRole: null
  }),
  actions: {
    async fetchRoles() {
      this.loading = true
      try {
        await ensureConfigLoaded()
        logger.debug("Fetching roles...")
        const response = await roleApi.fetchRoles()
        logger.debug("Roles API response:", response)

        // 适配后端API响应结构 (BaseResponse包装)
        if (response.data && response.data.data) {
          // 后端API返回的结构: { data: { data: [roles] } }
          this.list = response.data.data || []
          logger.info("Loaded roles from backend API", { total: this.list.length })
        } else if (response.data && Array.isArray(response.data)) {
          // Mock数据或直接返回的结构: { data: [roles] }
          this.list = response.data || []
          logger.info("Loaded roles from mock/direct API", { total: this.list.length })
        } else {
          logger.warn("Unexpected API response structure:", response)
          this.list = []
        }
      } catch (error) {
        logger.error("Failed to load roles", error)
        this.list = []
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchRoleDetail(id) {
      this.loading = true
      try {
        await ensureConfigLoaded()
        const response = await roleApi.fetchRole(id)
        logger.debug("Role detail API response:", response)

        // 适配后端API响应结构
        const roleData = response.data?.data || response.data
        this.currentRole = roleData
        logger.info("Loaded role detail", { id, name: roleData?.displayName })
        return roleData
      } catch (error) {
        logger.error("Failed to load role detail", { id, error })
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateRole(id, payload) {
      this.loading = true
      try {
        await ensureConfigLoaded()
        const response = await roleApi.updateRole(id, payload)
        logger.debug("Update role API response:", response)

        // 适配后端API响应结构
        const roleData = response.data?.data || response.data
        this.currentRole = roleData
        this.list = this.list.map((item) => (item.id === roleData.id ? roleData : item))
        logger.info("Role updated", { id, name: roleData?.displayName })
        return roleData
      } catch (error) {
        logger.error("Failed to update role", { id, error })
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
