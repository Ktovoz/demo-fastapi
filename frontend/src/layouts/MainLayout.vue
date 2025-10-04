<template>
  <a-layout class="main-layout">
    <Sidebar />
    <a-layout>
      <Header />
      <a-layout-content class="layout-content">
        <PageContainer :title="route.meta?.title" :description="route.meta?.description">
          <router-view />
        </PageContainer>
      </a-layout-content>
      <Footer />
    </a-layout>
  </a-layout>
</template>

<script setup>
import { useRoute } from 'vue-router'
import Header from '../components/layout/Header.vue'
import Sidebar from '../components/layout/Sidebar.vue'
import Footer from '../components/layout/Footer.vue'
import PageContainer from '../components/layout/PageContainer.vue'

const route = useRoute()
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
}

.layout-content {
  background: #f5f7fa;
}
</style>
