import { defineStore } from "pinia"
import { authApi } from "../api/auth"
import { createLogger } from "../utils/logger"

const logger = createLogger("AuthStore")
const STORAGE_KEY = "demo_fastapi_session"

const readStoredSession = () => {
  if (typeof window === "undefined") return null
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch (error) {
    logger.warn("Failed to read stored session", error)
    return null
  }
}

const writeStoredSession = (session) => {
  if (typeof window === "undefined") return
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(session))
  } catch (error) {
    logger.warn("Failed to persist session", error)
  }
}

const clearStoredSession = () => {
  if (typeof window === "undefined") return
  try {
    window.localStorage.removeItem(STORAGE_KEY)
  } catch (error) {
    logger.warn("Failed to clear session", error)
  }
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: null,
    user: null,
    loading: false,
    expiresAt: null,
    initialized: false
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
    userName: (state) => state.user?.name ?? "",
    permissions: (state) => state.user?.permissions ?? []
  },
  actions: {
    async restoreSession() {
      if (this.initialized) return
      const stored = readStoredSession()
      if (stored?.token && (!stored.expiresAt || stored.expiresAt > Date.now())) {
        this.token = stored.token
        this.user = stored.user
        this.expiresAt = stored.expiresAt ?? null
        logger.info("Restored session from storage")
      } else if (stored?.token) {
        logger.info("Stored session expired, clearing")
        clearStoredSession()
      }
      this.initialized = true
    },

    async login(credentials) {
      this.loading = true
      try {
        logger.debug("开始登录流程", { email: credentials.email })
        const response = await authApi.login(credentials)
        logger.debug("登录API响应:", response)

        // 修复数据访问路径：后端返回的是 { success: true, data: { token, user, expiresIn } }
        const responseData = response.data.data || response.data
        const { token, user, expiresIn } = responseData

        this.token = token
        this.user = user
        this.expiresAt = expiresIn ? Date.now() + expiresIn * 60 * 1000 : null
        writeStoredSession({ token: this.token, user: this.user, expiresAt: this.expiresAt })
        logger.info("User logged in", { email: user.email, userId: user.id })
      } catch (error) {
        logger.error("Login failed", error)
        // 提取更详细的错误信息
        const errorMessage = error.response?.data?.detail || error.message || '登录失败'
        logger.error("详细错误信息:", {
          status: error.response?.status,
          data: error.response?.data,
          message: errorMessage
        })
        throw new Error(errorMessage)
      } finally {
        this.loading = false
        this.initialized = true
      }
    },

    async register(userData) {
      this.loading = true
      try {
        logger.debug("开始注册流程", { email: userData.email, name: userData.name })
        logger.debug("注册请求数据:", userData)
        const response = await authApi.register(userData)
        logger.debug("注册API响应:", response)

        // 修复数据访问路径：后端返回的是 { success: true, data: {...} }
        const responseData = response.data.data || response.data

        logger.info("用户注册成功", {
          email: userData.email,
          userId: responseData.id,
          message: response.data.message
        })

        return responseData
      } catch (error) {
        logger.error("Register failed", error)
        // 提取更详细的错误信息
        const errorMessage = error.response?.data?.detail || error.message || '注册失败'
        logger.error("详细错误信息:", {
          status: error.response?.status,
          data: error.response?.data,
          message: errorMessage
        })
        // 对于422错误，通常是验证错误，尝试获取更详细的验证错误
        if (error.response?.status === 422) {
          logger.error("422验证错误详情:", error.response?.data)
          const validationErrors = error.response?.data?.detail || []
          if (Array.isArray(validationErrors)) {
            validationErrors.forEach((err, idx) => {
              logger.error(`验证错误 ${idx + 1}:`, err)
            })
          }
        }
        throw new Error(errorMessage)
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.token = null
      this.user = null
      this.expiresAt = null
      clearStoredSession()
      logger.info("User logged out")
    },

    hasPermission(permission) {
      if (!permission) return true
      const permissions = this.permissions
      if (!permissions || permissions.length === 0) return false
      if (permissions.includes("*")) return true
      return permissions.includes(permission)
    }
  }
})
