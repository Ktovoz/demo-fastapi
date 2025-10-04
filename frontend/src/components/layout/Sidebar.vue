<template>
  <a-layout-sider
    class="layout-sider"
    :collapsed="menuCollapsed"
    collapsible
    @collapse="handleCollapse"
  >
    <div class="logo">Demo</div>
    <a-menu
      theme="dark"
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
  FileSearchOutlined
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

const derivedOpenKeys = computed(() => (currentNode.value?.parents ?? []))

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
  min-height: 100vh;
}

.logo {
  height: 48px;
  margin: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #fff;
}
</style>
