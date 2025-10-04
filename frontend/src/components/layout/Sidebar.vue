<template>
  <a-layout-sider
    :class="sidebarClasses"
    :collapsed="menuCollapsed"
    collapsible
    :trigger="null"
    @collapse="handleCollapse"
  >
    <div class="logo">
      <span class="logo__text">Demo</span>
      <a-button type="text" class="logo__toggle" @click="toggleSidebar">
        <component :is="menuCollapsed ? MenuUnfoldOutlined : MenuFoldOutlined" />
      </a-button>
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
  MenuFoldOutlined,
  MenuUnfoldOutlined
} from '@ant-design/icons-vue'
import { useSystemStore } from '../../store/system'
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

const systemStore = useSystemStore()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const menuCollapsed = computed(() => systemStore.menuCollapsed)
const menuTheme = computed(() => (systemStore.theme === 'dark' ? 'dark' : 'light'))
const sidebarClasses = computed(() => [
  'layout-sider',
  menuCollapsed.value ? 'layout-sider--collapsed' : 'layout-sider--expanded',
  menuTheme.value === 'dark' ? 'layout-sider--dark' : 'layout-sider--light'
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

const toggleSidebar = () => {
  const next = !menuCollapsed.value
  if (typeof systemStore.setMenuCollapsed === 'function') {
    systemStore.setMenuCollapsed(next)
  } else {
    systemStore.menuCollapsed = next
  }
}

const handleSelect = ({ key }) => {
  const node = findNavigationNode((item) => item.key === key, navigationTree)
  const path = node?.item?.path
  if (path) {
    router.push(path)
  }
}

const handleOpenChange = (keys) => {
  openKeys.value = keys
}

const handleCollapse = (value) => {
  if (typeof systemStore.setMenuCollapsed === 'function') {
    systemStore.setMenuCollapsed(value)
  } else {
    systemStore.menuCollapsed = value
  }
}
</script>

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
  padding-inline: 0 !important;
  padding-block: 14px !important;
  margin: 10px 12px;
  display: flex !important;
  justify-content: center;
  align-items: center;
  border-radius: 20px;
}


.logo__toggle {
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  color: #1d4ed8;
  border: 1px solid rgba(37, 99, 235, 0.18);
  background: rgba(59, 130, 246, 0.08);
  transition: all 0.2s ease;
}

.logo__toggle :deep(.anticon) {
  font-size: 18px;
}

.logo__toggle:hover {
  color: #2563eb;
  background: rgba(59, 130, 246, 0.16);
  border-color: rgba(59, 130, 246, 0.25);
}

.layout-sider--collapsed .logo {
  justify-content: center;
  padding: 6px;
}

.layout-sider--collapsed .logo__text {
  display: none;
}

.layout-sider--collapsed .logo__toggle {
  width: 36px;
  height: 36px;
}

.sidebar-menu {
  width: 100%;
  flex: 1;
}


</style>
