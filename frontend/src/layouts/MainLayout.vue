<template>
  <a-layout class="main-layout" :class="[`theme-${theme}`]">
    <Sidebar />
    <a-layout class="main-layout__content">
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
  position: relative;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #0f172a 100%);
  overflow: hidden;
}

.main-layout::before,
.main-layout::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.4;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.main-layout::before {
  width: 480px;
  height: 480px;
  top: -160px;
  left: -120px;
  background: rgba(59, 130, 246, 0.45);
}

.main-layout::after {
  width: 420px;
  height: 420px;
  right: -160px;
  bottom: -140px;
  background: rgba(236, 72, 153, 0.4);
}

.main-layout__content {
  position: relative;
  z-index: 1;
  background: transparent;
}

.layout-content {
  position: relative;
  background: transparent;
  padding: 0;
}

.theme-dark .layout-content {
  background: transparent;
}

.theme-dark .page-container {
  color: #f8fafc;
}

@media (max-width: 1024px) {
  .main-layout::before {
    width: 340px;
    height: 340px;
    top: -140px;
    left: -160px;
  }

  .main-layout::after {
    width: 320px;
    height: 320px;
    right: -140px;
    bottom: -160px;
  }
}
</style>
