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
      @openChange="(keys) => (openKeys = keys)"
      @select="handleSelect"
      :items="menuItems"
    />
  </a-layout-sider>
</template>

<script setup>
import { computed, h, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import {
  DashboardOutlined,
  TeamOutlined,
  SafetyOutlined,
  SettingOutlined,
  ProfileOutlined,
  FileSearchOutlined
} from "@ant-design/icons-vue"
import { useSystemStore } from "../../store/system"
import { useAuthStore } from "../../store/auth"

const systemStore = useSystemStore()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const menuCollapsed = computed(() => systemStore.menuCollapsed)

const rawMenu = [
  {
    key: "dashboard",
    icon: () => h(DashboardOutlined),
    label: "Dashboard",
    path: "/dashboard",
    permission: "dashboard:view"
  },
  {
    key: "users",
    icon: () => h(TeamOutlined),
    label: "Users",
    path: "/users/list",
    permission: "users:view"
  },
  {
    key: "roles",
    icon: () => h(SafetyOutlined),
    label: "Roles",
    path: "/roles/list",
    permission: "roles:view"
  },
  {
    key: "system",
    icon: () => h(SettingOutlined),
    label: "System",
    children: [
      {
        key: "system-logs",
        icon: () => h(FileSearchOutlined),
        label: "Logs",
        path: "/system/logs",
        permission: "logs:view"
      },
      {
        key: "system-settings",
        icon: () => h(SettingOutlined),
        label: "Settings",
        path: "/system/settings",
        permission: "system:manage"
      }
    ]
  },
  {
    key: "profile",
    icon: () => h(ProfileOutlined),
    label: "Profile",
    path: "/profile",
    permission: "users:view"
  }
]

const hasPermission = (item) => {
  if (!item.permission) return true
  return authStore.hasPermission(item.permission)
}

const mapMenu = (items) => {
  return items
    .filter((item) => hasPermission(item))
    .map((item) => {
      if (item.children) {
        const children = mapMenu(item.children)
        return { ...item, children }
      }
      return item
    })
    .filter((item) => (item.children ? item.children.length > 0 : true))
}

const menuItems = computed(() => mapMenu(rawMenu))

const resolveMenuItem = (items, matcher) => {
  for (const item of items) {
    if (matcher(item)) return item
    if (item.children) {
      const child = resolveMenuItem(item.children, matcher)
      if (child) return child
    }
  }
  return null
}

const selectedKeys = computed(() => {
  const match = resolveMenuItem(menuItems.value, (item) =>
    item.path ? route.path.startsWith(item.path) : false
  )
  return match ? [match.key] : []
})

const openKeys = ref([])

watch(
  () => route.path,
  () => {
    const parent = menuItems.value.find((item) =>
      item.children?.some((child) => route.path.startsWith(child.path || ""))
    )
    if (parent) {
      openKeys.value = [parent.key]
    }
  },
  { immediate: true }
)

const handleSelect = ({ key }) => {
  const target = resolveMenuItem(menuItems.value, (item) => item.key === key)
  if (target?.path) {
    router.push(target.path)
  }
}

const handleCollapse = (value) => {
  systemStore.menuCollapsed = value
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
