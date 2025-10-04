<template>
  <div id="app">
    <a-layout class="layout">
      <a-layout-header>
        <div class="logo">Demo FastAPI</div>
        <a-menu
          theme="dark"
          mode="horizontal"
          :default-selected-keys="['1']"
          style="line-height: 64px;"
        >
          <a-menu-item key="1">
            <router-link to="/">首页</router-link>
          </a-menu-item>
          <a-menu-item key="2">
            <router-link to="/about">关于</router-link>
          </a-menu-item>
        </a-menu>
      </a-layout-header>
      <a-layout-content style="padding: 0 50px;">
        <div class="site-layout-content" :style="{ padding: '24px', minHeight: '280px' }">
          <router-view />
        </div>
      </a-layout-content>
      <a-layout-footer style="text-align: center">
        FastAPI + Vue Demo ©2024 Created by Your Name
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<script setup>
// App component logic
</script>

<style scoped>
.logo {
  float: left;
  width: 120px;
  height: 31px;
  margin: 16px 24px 16px 0;
  color: white;
  font-size: 18px;
  font-weight: bold;
}

.site-layout-content {
  background: #fff;
  padding: 24px;
  min-height: 280px;
}
</style>