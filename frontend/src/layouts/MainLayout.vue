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
  background: linear-gradient(140deg, #eef2ff 0%, #f8fafc 45%, #e2e8f0 100%);
}

.main-layout::before,
.main-layout::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.35;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.main-layout::before {
  width: 420px;
  height: 420px;
  top: -160px;
  left: -140px;
  background: rgba(59, 130, 246, 0.35);
}

.main-layout::after {
  width: 360px;
  height: 360px;
  right: -140px;
  bottom: -160px;
  background: rgba(236, 72, 153, 0.3);
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
    width: 320px;
    height: 320px;
    top: -140px;
    left: -120px;
  }

  .main-layout::after {
    width: 280px;
    height: 280px;
    right: -120px;
    bottom: -140px;
  }
}
</style>
