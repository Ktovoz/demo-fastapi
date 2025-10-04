import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'
import DashboardIndex from '../views/dashboard/Index.vue'
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'
import ForgotPassword from '../views/auth/ForgotPassword.vue'
import UserList from '../views/users/UserList.vue'
import UserDetail from '../views/users/UserDetail.vue'
import UserEdit from '../views/users/UserEdit.vue'
import RoleList from '../views/roles/RoleList.vue'
import RoleEdit from '../views/roles/RoleEdit.vue'
import SystemLogs from '../views/system/Logs.vue'
import SystemSettings from '../views/system/Settings.vue'
import Profile from '../views/profile/Profile.vue'
import Forbidden from '../views/error/Forbidden.vue'
import NotFound from '../views/error/NotFound.vue'
import { createLogger } from '../utils/logger'

const logger = createLogger('Router')

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/auth/login',
    name: 'AuthLogin',
    component: Login,
    meta: { title: 'Login', public: true }
  },
  {
    path: '/auth/register',
    name: 'AuthRegister',
    component: Register,
    meta: { title: 'Register', public: true }
  },
  {
    path: '/auth/forgot-password',
    name: 'AuthForgotPassword',
    component: ForgotPassword,
    meta: { title: 'Forgot Password', public: true }
  },
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: DashboardIndex,
        meta: { title: 'Dashboard', description: 'Key performance indicators and recent activity.' }
      },
      {
        path: 'users',
        redirect: '/users/list'
      },
      {
        path: 'users/list',
        name: 'UserList',
        component: UserList,
        meta: { title: 'Users', description: 'Manage platform users and their permissions.' }
      },
      {
        path: 'users/:id',
        name: 'UserDetail',
        component: UserDetail,
        meta: { title: 'User Detail' }
      },
      {
        path: 'users/:id/edit',
        name: 'UserEdit',
        component: UserEdit,
        meta: { title: 'Edit User' }
      },
      {
        path: 'roles',
        redirect: '/roles/list'
      },
      {
        path: 'roles/list',
        name: 'RoleList',
        component: RoleList,
        meta: { title: 'Roles', description: 'Configure application roles and permissions.' }
      },
      {
        path: 'roles/:id/edit',
        name: 'RoleEdit',
        component: RoleEdit,
        meta: { title: 'Edit Role' }
      },
      {
        path: 'system/logs',
        name: 'SystemLogs',
        component: SystemLogs,
        meta: { title: 'System Logs' }
      },
      {
        path: 'system/settings',
        name: 'SystemSettings',
        component: SystemSettings,
        meta: { title: 'System Settings' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: Profile,
        meta: { title: 'Profile' }
      }
    ]
  },
  {
    path: '/403',
    name: 'Forbidden',
    component: Forbidden,
    meta: { title: 'Forbidden', public: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { title: 'Not Found', public: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach((to, from, next) => {
  logger.info(`Navigating: ${from.fullPath || 'start'} -> ${to.fullPath}`)

  if (to.meta?.title) {
    document.title = `${to.meta.title} - Demo FastAPI`
  }

  next()
})

router.afterEach((to) => {
  logger.info(`Navigation complete: ${to.fullPath}`)
})

export default router
