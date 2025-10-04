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
        const response = await authApi.login(credentials)
        const { token, user, expiresIn } = response.data
        this.token = token
        this.user = user
        this.expiresAt = expiresIn ? Date.now() + expiresIn * 60 * 1000 : null
        writeStoredSession({ token: this.token, user: this.user, expiresAt: this.expiresAt })
        logger.info("User logged in", { email: user.email })
      } catch (error) {
        logger.error("Login failed", error)
        throw error
      } finally {
        this.loading = false
        this.initialized = true
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
