import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import { createLogger } from '../utils/logger'

// 创建路由日志器
const logger = createLogger('Router')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: '首页'
    }
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    meta: {
      title: '关于'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  logger.info(`🧭 路由跳转: ${from.path} -> ${to.path}`)

  // 设置页面标题
  if (to.meta?.title) {
    document.title = `${to.meta.title} - Demo FastAPI`
  }

  next()
})

// 全局后置钩子
router.afterEach((to, from) => {
  logger.info(`✅ 路由跳转完成: ${to.path}`)
})

export default router