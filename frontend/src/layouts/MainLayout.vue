<template>
  <a-layout class="main-layout" :class="[`theme-${theme}`]">
    <Sidebar />
    <a-layout>
      <Header />
      <a-layout-content class="layout-content">
        <PageContainer
          :title="pageTitle"
          :description="pageDescription"
          :breadcrumbs="breadcrumbs"
        >
          <router-view />
        </PageContainer>
      </a-layout-content>
      <Footer />
    </a-layout>
  </a-layout>
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import Header from "../components/layout/Header.vue"
import Sidebar from "../components/layout/Sidebar.vue"
import Footer from "../components/layout/Footer.vue"
import PageContainer from "../components/layout/PageContainer.vue"
import { useSystemStore } from "../store/system"

const route = useRoute()
const systemStore = useSystemStore()

const pageTitle = computed(() => route.meta?.title ?? "")
const pageDescription = computed(() => route.meta?.description ?? "")
const breadcrumbs = computed(() => route.meta?.breadcrumb ?? [])
const theme = computed(() => systemStore.theme)
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
}

.layout-content {
  background: #f5f7fa;
}

.theme-dark .layout-content {
  background: #0f172a;
}
</style>
