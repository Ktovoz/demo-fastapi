<template>
  <div class="about">
    <a-page-header
      title="关于项目"
      sub-title="FastAPI + Vue 前后端分离示例"
      @back="() => $router.go(-1)"
    />

    <a-row :gutter="16" style="margin-top: 24px;">
      <a-col :span="12">
        <a-card title="技术栈" :bordered="false">
          <h3>前端技术</h3>
          <ul>
            <li>Vue 3 - 渐进式 JavaScript 框架</li>
            <li>Ant Design Vue - 企业级 UI 设计语言</li>
            <li>Vite - 新一代前端构建工具</li>
            <li>Vue Router - Vue.js 官方路由</li>
            <li>Pinia - Vue 的状态管理库</li>
            <li>Axios - HTTP 请求库</li>
          </ul>

          <h3>后端技术</h3>
          <ul>
            <li>FastAPI - 现代、快速的 Web 框架</li>
            <li>Python - 编程语言</li>
            <li>Uvicorn - ASGI 服务器</li>
          </ul>
        </a-card>
      </a-col>

      <a-col :span="12">
        <a-card title="项目特性" :bordered="false">
          <a-list item-layout="horizontal" :data-source="features">
            <template #renderItem="{ item }">
              <a-list-item>
                <a-list-item-meta
                  :description="item.description"
                >
                  <template #title>
                    <span>{{ item.title }}</span>
                  </template>
                  <template #avatar>
                    <a-avatar style="background-color: #1890ff" :icon="item.icon" />
                  </template>
                </a-list-item-meta>
              </a-list-item>
            </template>
          </a-list>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const features = ref([
  {
    title: '前后端分离',
    description: '采用前后端分离架构，提高开发效率和代码可维护性',
    icon: 'code'
  },
  {
    title: 'RESTful API',
    description: '标准的 REST API 设计，支持各种客户端接入',
    icon: 'api'
  },
  {
    title: '现代化 UI',
    description: '使用 Ant Design Vue 提供美观的用户界面',
    icon: 'layout'
  },
  {
    title: '快速开发',
    description: '基于 Vite 的快速构建和热重载开发体验',
    icon: 'thunderbolt'
  }
])
</script>

<style scoped>
.about {
  padding: 20px;
}
</style>