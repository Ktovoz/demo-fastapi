<template>
  <a-layout-sider
    :class="sidebarClasses"
    :collapsed="menuCollapsed"
    collapsible
  >
  >
    <div class="logo">
      <span class="logo__text">Demo</span>
    </div>
    <a-menu
      class="sidebar-menu"
      :theme="menuTheme"
      mode="inline"
      :selected-keys="selectedKeys"
      :open-keys="openKeys"
      :items="menuItems"
      @openChange="handleOpenChange"
      @select="handleSelect"
    />
  </a-layout-sider>
</template>

<script setup>
import { computed, h, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  DashboardOutlined,
  TeamOutlined,
  SafetyOutlined,
  SettingOutlined,
  ProfileOutlined,
  FileSearchOutlined,
import { useAuthStore } from '../../store/auth'
import { navigationTree, findNavigationNode, findNavigationByPath } from '../../config/navigation'

const iconRegistry = {
  DashboardOutlined,
  TeamOutlined,
  SafetyOutlined,
  SettingOutlined,
  ProfileOutlined,
  FileSearchOutlined
}

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const menuCollapsed = ref(false)
const menuTheme = ref('light')
const sidebarClasses = computed(() => [
  'layout-sider',
  menuCollapsed.value ? 'layout-sider--collapsed' : 'layout-sider--expanded',
  'layout-sider--light'
])

const hasPermission = (item) => {
  if (!item.permission) return true
  return authStore.hasPermission(item.permission)
}

const resolveIcon = (iconName) => {
  const component = iconRegistry[iconName]
  return component ? () => h(component) : undefined
}

const normalizeMenuItems = (items) =>
  items
    .filter(hasPermission)
    .map((item) => {
      const normalized = {
        key: item.key,
        label: item.label,
        icon: resolveIcon(item.icon)
      }
      if (item.children?.length) {
        const children = normalizeMenuItems(item.children)
        if (children.length === 0) {
          return null
        }
        normalized.children = children
      } else {
        normalized.path = item.path
      }
      return normalized
    })
    .filter(Boolean)

const menuItems = computed(() => normalizeMenuItems(navigationTree))

const openKeys = ref([])

const currentNode = computed(() => {
  if (route.meta?.menuKey) {
    const found = findNavigationNode((item) => item.key === route.meta.menuKey, navigationTree)
    if (found) return found
  }
  return findNavigationByPath(route.path)
})

const selectedKeys = computed(() => {
  const key = currentNode.value?.item?.key
  return key ? [key] : []
})

const derivedOpenKeys = computed(() => currentNode.value?.parents ?? [])

watch(
  derivedOpenKeys,
  (keys) => {
    if (!menuCollapsed.value) {
      openKeys.value = keys
    }
  },
  { immediate: true }
)

watch(menuCollapsed, (collapsed) => {
  openKeys.value = collapsed ? [] : derivedOpenKeys.value
})

  }
}

const handleOpenChange = (keys) => {
  openKeys.value = keys
}

}

<style scoped>
.layout-sider {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 100vh;
  padding: 28px 22px 32px;
  gap: 20px;
  transition: background 0.3s ease, box-shadow 0.3s ease, width 0.2s ease;
  border-right: 1px solid rgba(148, 163, 184, 0.18);
  backdrop-filter: blur(22px);
}

.layout-sider::before,
.layout-sider::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.65;
  transition: opacity 0.3s ease;
}

.layout-sider::before {
  background: radial-gradient(circle at 20% 10%, rgba(59, 130, 246, 0.25), transparent 55%);
}

.layout-sider::after {
  background: radial-gradient(circle at 80% 90%, rgba(14, 165, 233, 0.18), transparent 60%);
}

.layout-sider--dark {
  background: linear-gradient(160deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.92));
  border-right-color: rgba(30, 41, 59, 0.6);
}

.layout-sider--light {
  background: linear-gradient(160deg, rgba(241, 245, 249, 0.92), rgba(226, 232, 240, 0.88));
  border-right-color: rgba(148, 163, 184, 0.4);
}

.layout-sider--collapsed {
  padding-inline: 16px;
}

.logo {
  position: relative;
  z-index: 1;
  height: 52px;
  margin-bottom: 20px;
  padding: 0 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #0f172a;
  background: rgba(255, 255, 255, 0.78);
  border-radius: 16px;
  box-shadow: 0 10px 22px rgba(15, 23, 42, 0.12);
}

.layout-sider--dark .logo {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.28), rgba(129, 140, 248, 0.42));
  color: #e2e8f0;
  box-shadow: 0 16px 28px rgba(15, 23, 42, 0.35);
}

.layout-sider--collapsed .logo {
  font-size: 14px;
  letter-spacing: 0.12em;
}

.sidebar-menu {
  position: relative;
  z-index: 1;
  border: none;
  background: transparent;
}

.sidebar-menu :deep(.ant-menu-item),
.sidebar-menu :deep(.ant-menu-submenu-title) {
  border-radius: 12px;
  margin-inline: 4px;
  margin-block: 2px;
  padding-inline: 16px !important;
  padding-block: 10px !important;
  margin-inline: 6px;
  margin-block: 4px;
  transition: background 0.2s ease, color 0.2s ease;
}

.sidebar-menu :deep(.ant-menu-light .ant-menu-item:hover),
.sidebar-menu :deep(.ant-menu-light .ant-menu-submenu-title:hover) {
  background: rgba(59, 130, 246, 0.12);
  color: #1d4ed8;
}

.sidebar-menu :deep(.ant-menu-item-selected) {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.18), rgba(14, 165, 233, 0.14));
  color: #1d4ed8;
  box-shadow: inset 0 0 0 1px rgba(59, 130, 246, 0.28);
}

.sidebar-menu :deep(.ant-menu-dark) {
  background: transparent;
}

.sidebar-menu :deep(.ant-menu-dark .ant-menu-item-selected) {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.28), rgba(79, 70, 229, 0.3));
  color: #f8fafc;
}

.sidebar-menu :deep(.ant-menu-submenu-arrow) {
  color: inherit;
}

.sidebar-menu :deep(.ant-menu-item-group-title) {
  padding-inline-start: 12px;
  font-size: 12px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.sidebar-menu :deep(.ant-menu-inline) {
  border-inline-end: none !important;
}

.sidebar-menu :deep(.ant-menu-inline-collapsed .ant-menu-item),
.sidebar-menu :deep(.ant-menu-inline-collapsed .ant-menu-submenu-title) {
  padding: 0 !important;
  margin: 6px 12px;
  display: grid !important;
  place-items: center;
  border-radius: 20px;
  width: 40px !important;
  height: 40px !important;
}

.sidebar-menu :deep(.ant-menu-inline-collapsed .ant-menu-item .anticon),
.sidebar-menu :deep(.ant-menu-inline-collapsed .ant-menu-submenu-title .anticon) {
  font-size: 18px !important;
  margin: 0 !important;
  display: grid !important;
  place-items: center;
  width: 100% !important;
  height: 100% !important;
}


.sidebar-menu {
  width: 100%;
  flex: 1;
}


</style>
