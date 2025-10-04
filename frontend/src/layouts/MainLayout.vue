<template>
  <AppShell :theme="theme" :sidebar-collapsed="menuCollapsed">
    <template #sidebar>
      <Sidebar />
    </template>

    <template #header>
      <Header />
    </template>

    <template #footer>
      <Footer />
    </template>

    <PageContainer :title="pageTitle" :description="pageDescription" :breadcrumbs="breadcrumbs" :hide-header="hideHeader">
      <router-view />
    </PageContainer>
  </AppShell>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppShell from '../components/layout/AppShell.vue'
import Header from '../components/layout/Header.vue'
import Sidebar from '../components/layout/Sidebar.vue'
import Footer from '../components/layout/Footer.vue'
import PageContainer from '../components/layout/PageContainer.vue'
import { useSystemStore } from '../store/system'

const route = useRoute()
const systemStore = useSystemStore()

const pageTitle = computed(() => route.meta?.title ?? '')
const pageDescription = computed(() => route.meta?.description ?? '')
const breadcrumbs = computed(() => route.meta?.breadcrumb ?? [])
const hideHeader = computed(() => Boolean(route.meta?.hideHeader))
const theme = computed(() => systemStore.theme)
const menuCollapsed = computed(() => systemStore.menuCollapsed)
</script>

<style scoped>
:global(body) {
  background: transparent;
}

.app-shell {
  --app-sidebar-width: 240px;
  --app-sidebar-width-collapsed: 88px;
  --header-height: 64px;
}
</style>
