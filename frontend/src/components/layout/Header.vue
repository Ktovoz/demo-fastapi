<template>
  <a-layout-header class="layout-header">
    <div class="header-left">
      <a-button type="text" class="trigger" @click="toggleMenu">
        <component :is="menuCollapsed ? MenuUnfoldOutlined : MenuFoldOutlined"/>
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
          class=" header-search
      "
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
        <a-badge :count="unreadCount" :offset="[ -2, 4 ]">
          <a-button type="text" class="icon-button">
            <BellOutlined/>
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
            <UserOutlined/>
          </a-avatar>
          <span class="user-name">{{ userName }}</span>
        </div>
      </a-dropdown>
    </div>
  </a-layout-header>
</template>

<script setup>
import {computed, ref} from "vue"
import {useRoute, useRouter} from "vue-router"
import {BellOutlined, MenuFoldOutlined, MenuUnfoldOutlined, UserOutlined} from "@ant-design/icons-vue"
import {useSystemStore} from "../../store/system"
import {useAuthStore} from "../../store/auth"

const systemStore = useSystemStore()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const search = ref("")

const menuCollapsed = computed(() => systemStore.menuCollapsed)
const notifications = computed(() => systemStore.notifications)
const unreadCount = computed(() => notifications.value.filter((item) => !item.read).length)
const userName = computed(() => authStore.user?.name ?? "User")
const pageTitle = computed(() => route.meta?.title || "Dashboard")

const toggleMenu = () => {
  systemStore.toggleMenu()
}

const handleMenuClick = ({key}) => {
  if (key === "logout") {
    authStore.logout()
    router.push({path: "/auth/login"})
  }
  if (key === "profile") {
    router.push({path: "/profile"})
  }
}

const handleSearch = (value) => {
  if (!value) return
  console.info("Global search", value)
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
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 22px;
  background: #ffffff;
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.65);
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
  color: #0f172a;
  gap: 14px;
}

.header-left,
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.trigger {
  color: inherit;
  border-radius: 10px;
  transition: background 0.2s ease, color 0.2s ease;
}

.trigger:hover {
  color: #1d4ed8;
  background: rgba(59, 130, 246, 0.08);
}

.trigger :deep(.anticon) {
  font-size: 20px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 4px 12px;
  border-radius: 12px;
  background: rgba(241, 245, 249, 0.7);
}

.brand-name {
  font-size: 17px;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: #0f172a;
}

.brand-divider {
  width: 1px;
  height: 16px;
  background: rgba(15, 23, 42, 0.16);
}

.page-title {
  font-size: 14px;
  font-weight: 500;
  color: #1f3c88;
}

.header-search {
  width: clamp(180px, 16vw, 240px);
}

.header-search :deep(.ant-input-affix-wrapper) {
  border-radius: 12px;
  border: 1px solid rgba(203, 213, 225, 0.9);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}

.header-search :deep(.ant-input-affix-wrapper:hover),
.header-search :deep(.ant-input-affix-wrapper-focused) {
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.12);
}

.icon-button {
  color: #0f172a;
  border-radius: 10px;
}

.icon-button:hover {
  background: rgba(59, 130, 246, 0.08);
  color: #1d4ed8;
}

.layout-header :deep(.ant-btn-text) {
  color: inherit;
}

.layout-header :deep(.ant-btn-text:hover) {
  color: #1d4ed8;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #0f172a;
  cursor: pointer;
  padding: 4px 10px;
  border-radius: 12px;
  background: rgba(241, 245, 249, 0.7);
  transition: background 0.2s ease;
}

.user-info:hover {
  background: rgba(219, 234, 254, 0.7);
}

.user-avatar {
  background: linear-gradient(135deg, #3b82f6, #6366f1);
  color: #fff;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
}

.notification-list {
  width: 260px;
  max-height: 320px;
  overflow-y: auto;
}

.notification-item {
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.notification-item.unread .notification-title {
  font-weight: 600;
}

.notification-title {
  color: #1f2937;
}

.notification-time {
  font-size: 12px;
  color: #6b7280;
}

.popover-title {
  font-weight: 600;
  color: #1f2937;
}

.empty {
  padding: 16px 0;
  text-align: center;
  color: #94a3b8;
}

@media (max-width: 992px) {
  .layout-header {
    padding: 0 16px;
    gap: 12px;
  }

  .header-right {
    gap: 12px;
  }

  .header-search {
    width: 170px;
  }
}

@media (max-width: 768px) {
  .layout-header {
    padding: 0 12px;
    gap: 10px;
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
    gap: 10px;
  }

  .brand {
    padding: 4px 8px;
  }

  .header-search {
    width: 100%;
  }
}
</style>



