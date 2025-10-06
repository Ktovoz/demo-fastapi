import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs'
import path from 'path'

// 插件：处理 config.js 中的环境变量（仅在preview模式下）
function handleConfigPlugin() {
  return {
    name: 'handle-config-plugin',
    configureServer(server) {
      // 开发模式下不处理，直接使用代理
    },
    configurePreviewServer(server) {
      server.middlewares.use('/config.js', (req, res, next) => {
        if (req.method === 'GET') {
          const configPath = path.join(process.cwd(), 'public/config.js')
          let content = fs.readFileSync(configPath, 'utf8')
          let apiBaseUrl = process.env.VITE_API_BASE_URL || 'https://demo-fast-backend.ktovoz.com'
          // 自动添加协议前缀
          if (apiBaseUrl && !apiBaseUrl.startsWith('http://') && !apiBaseUrl.startsWith('https://')) {
            apiBaseUrl = 'https://' + apiBaseUrl
          }
          content = content.replace('${VITE_API_BASE_URL}', apiBaseUrl)
          res.setHeader('Content-Type', 'application/javascript')
          res.end(content)
        } else {
          next()
        }
      })
    }
  }
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    {
      name: 'handle-config-build',
      writeBundle() {
        // 构建完成后处理 dist/config.js 文件
        const configPath = path.join(process.cwd(), 'dist/config.js')

        if (fs.existsSync(configPath)) {
          let content = fs.readFileSync(configPath, 'utf8')
          let apiBaseUrl = process.env.VITE_API_BASE_URL || 'https://demo-fast-backend.ktovoz.com'

          console.log('替换环境变量:', { VITE_API_BASE_URL: process.env.VITE_API_BASE_URL, apiBaseUrl })

          // 自动添加协议前缀
          if (apiBaseUrl && !apiBaseUrl.startsWith('http://') && !apiBaseUrl.startsWith('https://')) {
            apiBaseUrl = 'https://' + apiBaseUrl
          }

          content = content.replace(/\$\{VITE_API_BASE_URL\}/g, apiBaseUrl)

          console.log('替换后的config.js内容:', content)

          fs.writeFileSync(configPath, content, 'utf8')
        }
      }
    },
    handleConfigPlugin()
  ],
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
      },
      '/health': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/health/, '/health')
      }
    }
  },
  preview: {
    port: 4173,
    host: '0.0.0.0',
    allowedHosts: ['demo-fast.ktovoz.com', 'localhost', '127.0.0.1'],
    proxy: {
      '/api': {
        target: (() => {
          let target = process.env.VITE_API_BASE_URL || 'https://demo-fast-backend.ktovoz.com'
          // 强制使用HTTPS协议
          if (target && target.startsWith('http://')) {
            console.log('🔧 Vite Preview: 转换HTTP目标到HTTPS:', target)
            target = target.replace('http://', 'https://')
          }
          // 确保有协议前缀
          if (target && !target.startsWith('http://') && !target.startsWith('https://')) {
            target = 'https://' + target
          }
          console.log('🔧 Vite Preview: 最终API代理目标:', target)
          return target
        })(),
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      },
      '/health': {
        target: (() => {
          let target = process.env.VITE_API_BASE_URL || 'https://demo-fast-backend.ktovoz.com'
          // 强制使用HTTPS协议
          if (target && target.startsWith('http://')) {
            console.log('🔧 Vite Preview: 转换HTTP目标到HTTPS:', target)
            target = target.replace('http://', 'https://')
          }
          // 确保有协议前缀
          if (target && !target.startsWith('http://') && !target.startsWith('https://')) {
            target = 'https://' + target
          }
          console.log('🔧 Vite Preview: 最终Health代理目标:', target)
          return target
        })(),
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/health/, '/health')
      }
    }
  }
})

