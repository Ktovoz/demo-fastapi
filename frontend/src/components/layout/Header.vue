<template>
  <a-layout-header :class="headerClasses">
    <div class="header-inner">
      <div class="header-left">
        <a-button type="text" class="trigger" @click="toggleMenu">
          <component :is="menuCollapsed ? MenuUnfoldOutlined : MenuFoldOutlined" />
        </a-button>
        <div class="brand">
          <slot name="logo">
            <span class="brand-name">Demo FastAPI Admin</span>
          </slot>
          <span class="brand-divider"></span>
          <span class="page-title">{{ pageTitle }}</span>
        </div>
      </div>
      <div class="header-right">
        <a-input-search
          v-model:value="search"
          placeholder="Search features or pages"
          allow-clear
          class="header-search"
          @search="handleSearch"
        />
        <a-popover placement="bottomRight" trigger="click">
          <template #title>
            <div class="popover-title">Notifications</div>
          </template>
          <template #content>
            <div class="notification-list">
              <div v-if="notifications.length === 0" class="empty">All caught up!</div>
              <template v-else>
                <div
                  v-for="item in notifications"
                  :key="item.id"
                  class="notification-item"
                  :class="{ unread: !item.read }"
                >
                  <div class="notification-title">{{ item.title }}</div>
                  <div class="notification-time">{{ item.time }}</div>
                </div>
                <a-button type="link" block @click="clearNotifications">Clear notifications</a-button>
              </template>
            </div>
          </template>
          <a-badge :count="unreadCount" :offset="[-2, 4]">
            <a-button type="text" class="icon-button">
              <BellOutlined />
            </a-button>
          </a-badge>
        </a-popover>
        <a-dropdown trigger="click">
          <template #overlay>
            <a-menu @click="handleMenuClick">
              <a-menu-item key="profile">Profile</a-menu-item>
              <a-menu-item key="logout">Logout</a-menu-item>
            </a-menu>
          </template>
          <div class="user-info">
            <a-avatar size="small" class="user-avatar">
              <UserOutlined />
            </a-avatar>
            <span class="user-name">{{ userName }}</span>
          </div>
        </a-dropdown>
      </div>
    </div>
  </a-layout-header>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { BellOutlined, MenuFoldOutlined, MenuUnfoldOutlined, UserOutlined } from '@ant-design/icons-vue'
import { useSystemStore } from '../../store/system'
import { useAuthStore } from '../../store/auth'

const systemStore = useSystemStore()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const search = ref('')

const headerTheme = computed(() => (systemStore.theme === 'dark' ? 'dark' : 'light'))
const headerClasses = computed(() => [
  'layout-header',
  headerTheme.value === 'dark' ? 'layout-header--dark' : 'layout-header--light'
])

const menuCollapsed = computed(() => systemStore.menuCollapsed)
const notifications = computed(() => systemStore.notifications)
const unreadCount = computed(() => notifications.value.filter((item) => !item.read).length)
const userName = computed(() => authStore.user?.name ?? 'User')
const pageTitle = computed(() => route.meta?.title || 'Dashboard')

const toggleMenu = () => {
  systemStore.toggleMenu()
}

const handleMenuClick = ({ key }) => {
  if (key === 'logout') {
    authStore.logout()
    router.push({ path: '/auth/login' })
  }
  if (key === 'profile') {
    router.push({ path: '/profile' })
  }
}

const handleSearch = (value) => {
  if (!value) return
  console.info('Global search', value)
}

const clearNotifications = () => {
  systemStore.clearNotifications()
}
</script>

<style scoped>
.layout-header {
  position: sticky;
  top: 0;
  z-index: 90;
  padding: 18px 42px;
  border-bottom: 1px solid rgba(148, 163, 184, 0.25);
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
  backdrop-filter: blur(16px);
  transition: background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

.layout-header--light {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.92), rgba(241, 245, 249, 0.85));
  color: #0f172a;
}

.layout-header :deep(.ant-btn-text) {
  color: inherit;
}

.layout-header :deep(.ant-btn-text:hover) {
  color: #2563eb;
}

.layout-header--dark :deep(.ant-btn-text:hover) {
  color: #93c5fd;
}

.layout-header--dark {
  background: linear-gradient(145deg, rgba(15, 23, 42, 0.92), rgba(30, 41, 59, 0.88));
  color: #e2e8f0;
  border-bottom-color: rgba(30, 41, 59, 0.55);
  box-shadow: 0 18px 32px rgba(15, 23, 42, 0.35);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  width: 100%;
  max-width: 1320px;
  margin: 0 auto;
  min-height: 58px;
}

.header-left,
.header-right {
  display: flex;
  align-items: center;
  gap: 18px;
}

.header-right {
  justify-content: flex-end;
}

.trigger {
  color: inherit;
  border-radius: 12px;
  transition: background 0.2s ease, color 0.2s ease;
}

.trigger:hover {
  color: #2563eb;
  background: rgba(37, 99, 235, 0.12);
}

.trigger :deep(.anticon) {
  font-size: 20px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 6px 16px;
  border-radius: 16px;
  background: rgba(37, 99, 235, 0.08);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(37, 99, 235, 0.14);
}

.layout-header--dark .brand {
  background: rgba(59, 130, 246, 0.16);
  border-color: rgba(125, 211, 252, 0.2);
}

.brand-name {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.brand-divider {
  width: 1px;
  height: 20px;
  background: rgba(15, 23, 42, 0.16);
}

.layout-header--dark .brand-divider {
  background: rgba(226, 232, 240, 0.3);
}

.page-title {
  font-size: 15px;
  font-weight: 500;
  color: inherit;
  opacity: 0.85;
}

.header-search {
  width: clamp(240px, 26vw, 360px);
}

.header-search :deep(.ant-input-affix-wrapper) {
  border-radius: 14px;
  border: 1px solid rgba(203, 213, 225, 0.8);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
}

.layout-header--dark .header-search :deep(.ant-input-affix-wrapper) {
  background: rgba(15, 23, 42, 0.65);
  border-color: rgba(148, 163, 184, 0.4);
  color: #e2e8f0;
}

.header-search :deep(.ant-input-affix-wrapper:hover),
.header-search :deep(.ant-input-affix-wrapper-focused) {
  border-color: rgba(59, 130, 246, 0.45);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.18);
}

.icon-button {
  color: inherit;
  border-radius: 12px;
}

.icon-button:hover {
  background: rgba(59, 130, 246, 0.12);
  color: #2563eb;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 14px;
  border-radius: 16px;
  background: rgba(241, 245, 249, 0.72);
  color: inherit;
  transition: background 0.2s ease;
}

.layout-header--dark .user-info {
  background: rgba(30, 41, 59, 0.7);
}

.user-info:hover {
  background: rgba(219, 234, 254, 0.9);
}

.layout-header--dark .user-info:hover {
  background: rgba(59, 130, 246, 0.28);
}

.user-avatar {
  background: linear-gradient(135deg, #3b82f6, #6366f1);
  color: #fff;
}

.user-name {
  font-size: 15px;
  font-weight: 500;
}

.notification-list {
  width: 280px;
  max-height: 340px;
  overflow-y: auto;
}

.notification-item {
  padding: 12px 0;
  border-bottom: 1px solid rgba(203, 213, 225, 0.5);
}

.notification-item.unread .notification-title {
  font-weight: 600;
}

.notification-title {
  color: inherit;
}

.notification-time {
  font-size: 12px;
  color: rgba(100, 116, 139, 0.85);
}

.popover-title {
  font-weight: 600;
  color: inherit;
}

.empty {
  padding: 18px 0;
  text-align: center;
  color: rgba(100, 116, 139, 0.7);
}

@media (max-width: 1280px) {
  .layout-header {
    padding: 16px 28px;
  }

  .header-inner {
    gap: 18px;
  }

  .header-search {
    width: clamp(220px, 32vw, 320px);
  }
}

@media (max-width: 992px) {
  .layout-header {
    padding: 14px 20px;
  }

  .header-inner {
    flex-wrap: wrap;
  }

  .header-left {
    width: 100%;
    justify-content: space-between;
  }

  .header-right {
    width: 100%;
    justify-content: flex-end;
    flex-wrap: wrap;
    gap: 12px;
  }

  .header-search {
    order: 3;
    width: 100%;
  }
}

@media (max-width: 576px) {
  .layout-header {
    padding: 12px 16px;
  }

  .brand {
    padding: 4px 10px;
  }

  .page-title {
    display: none;
  }
}
</style>
