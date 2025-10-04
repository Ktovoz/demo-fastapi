<template>
  <a-layout-sider class="layout-sider" collapsible v-model:collapsed="collapsed">
    <div class="logo">DF</div>
    <a-menu theme="dark" mode="inline" :selected-keys="selectedKeys">
      <a-menu-item v-for="item in menuItems" :key="item.key">
        <router-link :to="item.path">
          <span>{{ item.label }}</span>
        </router-link>
      </a-menu-item>
    </a-menu>
  </a-layout-sider>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const collapsed = ref(false)
const route = useRoute()

const menuItems = [
  { key: 'dashboard', path: '/dashboard', label: 'Dashboard' },
  { key: 'users', path: '/users/list', label: 'Users' },
  { key: 'roles', path: '/roles/list', label: 'Roles' },
  { key: 'system-logs', path: '/system/logs', label: 'System Logs' },
  { key: 'system-settings', path: '/system/settings', label: 'Settings' },
  { key: 'profile', path: '/profile', label: 'Profile' }
]

const selectedKeys = computed(() => {
  const current = menuItems.find(item => route.path.startsWith(item.path))
  return current ? [current.key] : []
})
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
