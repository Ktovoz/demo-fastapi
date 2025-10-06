import { defineStore } from "pinia"
import { roleApi } from "../api/role"
import { createLogger } from "../utils/logger"

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
        const response = await roleApi.fetchRoles()
        this.list = response.data
        logger.info("Loaded roles", { total: this.list.length })
      } catch (error) {
        logger.error("Failed to load roles", error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchRoleDetail(id) {
      this.loading = true
      try {
        const response = await roleApi.fetchRole(id)
        this.currentRole = response.data
        return response.data
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
        const response = await roleApi.updateRole(id, payload)
        this.currentRole = response.data
        this.list = this.list.map((item) => (item.id === response.data.id ? response.data : item))
        logger.info("Role updated", { id })
        return response.data
      } catch (error) {
        logger.error("Failed to update role", { id, error })
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
