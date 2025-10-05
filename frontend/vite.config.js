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
            // Group Ant Design Vue and icon packages together to avoid circular init timing issues
            if (id.includes('ant-design-vue') || id.includes('@ant-design/icons-vue')) {
              return 'antd'
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
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  },
  preview: {
    port: 4173,
    host: '0.0.0.0',
    allowedHosts: ['demo-fast.ktovoz.com', 'localhost', '127.0.0.1']
  }
})

