import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            // 将所有ant-design-vue相关模块打包在一起，避免模块间依赖问题
            if (id.includes('ant-design-vue')) {
              return 'antd'
            }
            // @ant-design/icons-vue 单独打包
            if (id.includes('@ant-design/icons-vue')) {
              return 'antd-icons'
            }
            // Vue相关模块打包在一起
            if (id.includes('vue')) {
              return 'vue'
            }
            // 日志相关模块
            if (id.includes('loglevel')) {
              return 'logging'
            }
          }
        }
      }
    },
    chunkSizeWarningLimit: 1000,
    // 优化模块解析
    modulePreload: {
      resolveDependencies(filename, deps) {
        return deps.filter(dep => !dep.includes('.map'))
      }
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  preview: {
    port: 4173,
    host: '0.0.0.0',
    allowedHosts: ['demo-fast.ktovoz.com', 'localhost', '127.0.0.1']
  }
})