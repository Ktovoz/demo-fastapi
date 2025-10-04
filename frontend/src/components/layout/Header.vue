<template>
  <a-layout-header class="layout-header">
    <div class="header-left">
      <a-button type="text" class="trigger" @click="toggleMenu">
        <component :is="menuCollapsed ? MenuUnfoldOutlined : MenuFoldOutlined" />
      </a-button>
      <div class="brand">
        <slot name="logo">Demo FastAPI Admin</slot>
        <span class="page-title">{{ pageTitle }}</span>
      </div>
    </div>
    <div class="header-right">
      <a-input-search
        v-model:value="search"
        placeholder="Quick search"
        allow-clear
        style="width: 220px"
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
          <a-button type="text"><BellOutlined /></a-button>
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
          <a-avatar size="small"><UserOutlined /></a-avatar>
          <span class="user-name">{{ userName }}</span>
        </div>
      </a-dropdown>
    </div>
  </a-layout-header>
</template>

<script setup>
import { computed, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { MenuFoldOutlined, MenuUnfoldOutlined, BellOutlined, UserOutlined } from "@ant-design/icons-vue"
import { useSystemStore } from "../../store/system"
import { useAuthStore } from "../../store/auth"

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

const handleMenuClick = ({ key }) => {
  if (key === "logout") {
    authStore.logout()
    router.push({ path: "/auth/login" })
  }
  if (key === "profile") {
    router.push({ path: "/profile" })
  }
}

const handleSearch = (value) => {
  if (!value) return
  // For now just log search intent; integrate with global search later
  console.info("Global search", value)
}

const clearNotifications = () => {
  systemStore.clearNotifications()
}
</script>

<style scoped>
.layout-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: #001529;
  color: #fff;
  gap: 16px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.trigger {
  color: inherit;
}

.trigger :deep(.anticon) {
  font-size: 20px;
}

.brand {
  display: flex;
  flex-direction: column;
}

.page-title {
  font-size: 14px;
  opacity: 0.75;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
  cursor: pointer;
}

.user-name {
  font-size: 14px;
}

.notification-list {
  width: 260px;
  max-height: 320px;
  overflow-y: auto;
}

.notification-item {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.notification-item.unread .notification-title {
  font-weight: 600;
}

.notification-title {
  color: #1f1f1f;
}

.notification-time {
  font-size: 12px;
  color: #8c8c8c;
}

.popover-title {
  font-weight: 600;
}

.empty {
  padding: 16px 0;
  text-align: center;
  color: #8c8c8c;
}
</style>
