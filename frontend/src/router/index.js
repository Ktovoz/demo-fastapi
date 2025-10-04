import { createRouter, createWebHistory } from "vue-router"
import MainLayout from "../layouts/MainLayout.vue"
import { createLogger } from "../utils/logger"
import { useAuthStore } from "../store/auth"
import { pinia } from "../store"

const logger = createLogger("Router")

const views = import.meta.glob('../views/**/*.vue')

const loadView = (path) => {
  const view = views[path]
  if (!view) {
    throw new Error(`View not found: ${path}`)
  }
  return view
}

const routes = [
  {
    path: "/",
    redirect: "/dashboard"
  },
  {
    path: "/auth/login",
    name: "AuthLogin",
    component: loadView("../views/auth/Login.vue"),
    meta: { title: "Login", public: true }
  },
  {
    path: "/auth/register",
    name: "AuthRegister",
    component: loadView("../views/auth/Register.vue"),
    meta: { title: "Register", public: true }
  },
  {
    path: "/auth/forgot-password",
    name: "AuthForgotPassword",
    component: loadView("../views/auth/ForgotPassword.vue"),
    meta: { title: "Forgot Password", public: true }
  },
  {
    path: "/",
    component: MainLayout,
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        component: loadView("../views/dashboard/Index.vue"),
        meta: {
          title: "Dashboard",
          description: "Key performance indicators and recent activity",
          breadcrumb: [{ label: "Dashboard" }],
          permission: "dashboard:view"
        }
      },
      {
        path: "users",
        redirect: "/users/list"
      },
      {
        path: "users/list",
        name: "UserList",
        component: loadView("../views/users/UserList.vue"),
        meta: {
          title: "Users",
          description: "Manage platform users and their permissions",
          breadcrumb: [{ label: "Users" }],
          permission: "users:view"
        }
      },
      {
        path: "users/create",
        name: "UserCreate",
        component: loadView("../views/users/UserEdit.vue"),
        meta: {
          title: "Create User",
          breadcrumb: [
            { label: "Users", to: "/users/list" },
            { label: "Create" }
          ],
          permission: "users:edit"
        }
      },
      {
        path: "users/:id",
        name: "UserDetail",
        component: loadView("../views/users/UserDetail.vue"),
        meta: {
          title: "User Detail",
          breadcrumb: [
            { label: "Users", to: "/users/list" },
            { label: "Profile" }
          ],
          permission: "users:view"
        }
      },
      {
        path: "users/:id/edit",
        name: "UserEdit",
        component: loadView("../views/users/UserEdit.vue"),
        meta: {
          title: "Edit User",
          breadcrumb: [
            { label: "Users", to: "/users/list" },
            { label: "Edit" }
          ],
          permission: "users:edit"
        }
      },
      {
        path: "roles",
        redirect: "/roles/list"
      },
      {
        path: "roles/list",
        name: "RoleList",
        component: loadView("../views/roles/RoleList.vue"),
        meta: {
          title: "Roles",
          description: "Configure application roles and permissions",
          breadcrumb: [{ label: "Roles" }],
          permission: "roles:view"
        }
      },
      {
        path: "roles/:id/edit",
        name: "RoleEdit",
        component: loadView("../views/roles/RoleEdit.vue"),
        meta: {
          title: "Edit Role",
          breadcrumb: [
            { label: "Roles", to: "/roles/list" },
            { label: "Edit" }
          ],
          permission: "roles:edit"
        }
      },
      {
        path: "system",
        redirect: "/system/overview"
      },
      {
        path: "system/overview",
        name: "SystemOverview",
        component: loadView("../views/system/AdminOverview.vue"),
        meta: {
          title: "Admin Overview",
          description: "Operations control center for the admin platform",
          breadcrumb: [
            { label: "System", to: "/system/overview" },
            { label: "Overview" }
          ],
          permission: "dashboard:view"
        }
      },
      {
        path: "system/logs",
        name: "SystemLogs",
        component: loadView("../views/system/Logs.vue"),
        meta: {
          title: "System Logs",
          breadcrumb: [
            { label: "System", to: "/system/overview" },
            { label: "Logs" }
          ],
          permission: "logs:view"
        }
      },
      {
        path: "system/settings",
        name: "SystemSettings",
        component: loadView("../views/system/Settings.vue"),
        meta: {
          title: "System Settings",
          breadcrumb: [
            { label: "System", to: "/system/overview" },
            { label: "Settings" }
          ],
          permission: "system:manage"
        }
      },
      {
        path: "profile",
        name: "Profile",
        component: loadView("../views/profile/Profile.vue"),
        meta: {
          title: "Profile",
          breadcrumb: [{ label: "Profile" }],
          permission: "users:view"
        }
      }
    ]
  },
  {
    path: "/403",
    name: "Forbidden",
    component: loadView("../views/error/Forbidden.vue"),
    meta: { title: "Forbidden", public: true }
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: loadView("../views/error/NotFound.vue"),
    meta: { title: "Not Found", public: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore(pinia)

  if (!authStore.initialized) {
    await authStore.restoreSession()
  }

  const requiresAuth = !to.meta?.public

  if (requiresAuth && !authStore.isAuthenticated) {
    logger.warn("Blocked navigation for unauthenticated user", { target: to.fullPath })
    return next({
      path: "/auth/login",
      query: { redirect: to.fullPath }
    })
  }

  if (to.meta?.permission && !authStore.hasPermission(to.meta.permission)) {
    logger.warn("Blocked navigation due to missing permission", {
      target: to.fullPath,
      permission: to.meta.permission
    })
    return next({ path: "/403" })
  }

  if (to.meta?.title) {
    document.title = `${to.meta.title} - Demo FastAPI`
  }

  logger.info(`Navigating: ${from.fullPath || 'start'} -> ${to.fullPath}`)
  next()
})

router.afterEach((to) => {
  logger.info(`Navigation complete: ${to.fullPath}`)
})

export default router

