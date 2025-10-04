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
            if (id.includes('ant-design-vue/es')) {
              const match = id.split('ant-design-vue/es/')[1]
              if (match) {
                const chunk = match.split('/')[0]
                return `antd-${chunk}`
              }
              return 'antd-shared'
            }
            if (id.includes('@ant-design/icons-vue')) {
              return 'antd-icons'
            }
            if (id.includes('vue')) {
              return 'vue'
            }
            if (id.includes('loglevel')) {
              return 'logging'
            }
          }
        }
      }
    },
    chunkSizeWarningLimit: 900
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
  }
})