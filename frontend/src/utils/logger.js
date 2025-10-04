import log from 'loglevel'
import prefix from 'loglevel-plugin-prefix'

// 日志级别
const LOG_LEVELS = {
  TRACE: 0,
  DEBUG: 1,
  INFO: 2,
  WARN: 3,
  ERROR: 4,
  SILENT: 5
}

// 日志颜色配置
const LOG_COLORS = {
  TRACE: '#7f8c8d',
  DEBUG: '#3498db',
  INFO: '#2ecc71',
  WARN: '#f39c12',
  ERROR: '#e74c3c'
}

// 前缀格式化函数
const formatPrefix = (level, name, timestamp) => {
  const colors = {
    TRACE: '#7f8c8d',
    DEBUG: '#3498db',
    INFO: '#2ecc71',
    WARN: '#f39c12',
    ERROR: '#e74c3c'
  }

  const color = colors[level.toUpperCase()]
  const time = new Date(timestamp).toLocaleTimeString()

  return [
    `%c${time}`,
    `%c[${level}]`,
    `%c${name || 'App'}:`
  ]
}

// 样式配置
const formatStyles = (level) => {
  const colors = {
    TRACE: 'color: #7f8c8d',
    DEBUG: 'color: #3498db',
    INFO: 'color: #2ecc71',
    WARN: 'color: #f39c12',
    ERROR: 'color: #e74c3c'
  }

  return [
    'color: #95a5a6; font-weight: bold',
    `color: ${colors[level]} ; font-weight: bold`,
    'color: #34495e; font-weight: bold'
  ]
}

class Logger {
  constructor() {
    this.isInitialized = false
    this.defaultLogger = null
    this.pendingLogs = [] // 存储待处理的日志
  }

  // 初始化日志系统
  init(options = {}) {
    if (this.isInitialized) {
      return this.defaultLogger
    }

    const {
      level = import.meta.env.DEV ? 'DEBUG' : 'INFO',
      prefixName = 'Demo App',
      enableConsole = true,
      enableStorage = false,
      storageKey = 'app_logs',
      maxStorageSize = 1000
    } = options

    try {
      // 应用前缀插件
      prefix.apply(log, {
        format: formatPrefix,
        levelFormatter: (level) => level.toUpperCase(),
        nameFormatter: (name) => name || prefixName,
        timestampFormatter: (date) => date.toISOString(),
        styleFormatter: formatStyles
      })

      // 设置日志级别
      log.setLevel(level)

      this.defaultLogger = log

      // 如果启用本地存储
      if (enableStorage && typeof localStorage !== 'undefined') {
        this.setupLocalStorage(storageKey, maxStorageSize)
      }

      // 初始化日志
      this.info('📝 日志系统已初始化', { level, prefix: prefixName, enableConsole, enableStorage })

      this.isInitialized = true

      // 处理待处理的日志
      this.processPendingLogs()

      return this.defaultLogger
    } catch (error) {
      console.error('日志系统初始化失败:', error)
      // 如果初始化失败，使用基本的 console 方法
      this.defaultLogger = this.createFallbackLogger()
      this.isInitialized = true
      return this.defaultLogger
    }
  }

  // 创建备用日志器
  createFallbackLogger() {
    return {
      trace: (...args) => console.log('[TRACE]', ...args),
      debug: (...args) => console.log('[DEBUG]', ...args),
      info: (...args) => console.info('[INFO]', ...args),
      warn: (...args) => console.warn('[WARN]', ...args),
      error: (...args) => console.error('[ERROR]', ...args)
    }
  }

  // 处理待处理的日志
  processPendingLogs() {
    if (this.pendingLogs.length > 0) {
      this.info(`📝 处理 ${this.pendingLogs.length} 条待处理日志`)
      this.pendingLogs.forEach(({ method, args }) => {
        this.defaultLogger[method](...args)
      })
      this.pendingLogs = []
    }
  }

  // 设置本地存储日志
  setupLocalStorage(key, maxSize) {
    const originalMethods = {}

    // 保存原始方法
    Object.keys(LOG_LEVELS).forEach(level => {
      if (level !== 'SILENT') {
        originalMethods[level] = log[level]
      }
    })

    // 重写日志方法
    Object.keys(LOG_LEVELS).forEach(level => {
      if (level !== 'SILENT') {
        log[level] = (...args) => {
          // 调用原始方法
          originalMethods[level].apply(log, args)

          // 保存到本地存储
          try {
            const logs = JSON.parse(localStorage.getItem(key) || '[]')
            const newLog = {
              timestamp: new Date().toISOString(),
              level,
              message: args.map(arg =>
                typeof arg === 'object' ? JSON.stringify(arg) : String(arg)
              ).join(' ')
            }

            logs.push(newLog)

            // 限制日志数量
            if (logs.length > maxSize) {
              logs.splice(0, logs.length - maxSize)
            }

            localStorage.setItem(key, JSON.stringify(logs))
          } catch (error) {
            console.error('保存日志到本地存储失败:', error)
          }
        }
      }
    })
  }

  // 获取本地存储的日志
  getStoredLogs(key = 'app_logs') {
    try {
      return JSON.parse(localStorage.getItem(key) || '[]')
    } catch (error) {
      console.error('读取本地存储日志失败:', error)
      return []
    }
  }

  // 清除本地存储的日志
  clearStoredLogs(key = 'app_logs') {
    try {
      localStorage.removeItem(key)
      this.info('🗑️ 本地日志已清除')
    } catch (error) {
      console.error('清除本地存储日志失败:', error)
    }
  }

  // 创建命名日志器
  getLogger(name) {
    // 如果还没初始化，先初始化
    if (!this.isInitialized) {
      this.init()
    }

    return {
      trace: (...args) => {
        if (this.isInitialized && this.defaultLogger) {
          this.defaultLogger.trace(...args, `[${name}]`)
        } else {
          this.pendingLogs.push({ method: 'trace', args: [...args, `[${name}]`] })
          console.log('[TRACE]', `[${name}]`, ...args)
        }
      },
      debug: (...args) => {
        if (this.isInitialized && this.defaultLogger) {
          this.defaultLogger.debug(...args, `[${name}]`)
        } else {
          this.pendingLogs.push({ method: 'debug', args: [...args, `[${name}]`] })
          console.log('[DEBUG]', `[${name}]`, ...args)
        }
      },
      info: (...args) => {
        if (this.isInitialized && this.defaultLogger) {
          this.defaultLogger.info(...args, `[${name}]`)
        } else {
          this.pendingLogs.push({ method: 'info', args: [...args, `[${name}]`] })
          console.info('[INFO]', `[${name}]`, ...args)
        }
      },
      warn: (...args) => {
        if (this.isInitialized && this.defaultLogger) {
          this.defaultLogger.warn(...args, `[${name}]`)
        } else {
          this.pendingLogs.push({ method: 'warn', args: [...args, `[${name}]`] })
          console.warn('[WARN]', `[${name}]`, ...args)
        }
      },
      error: (...args) => {
        if (this.isInitialized && this.defaultLogger) {
          this.defaultLogger.error(...args, `[${name}]`)
        } else {
          this.pendingLogs.push({ method: 'error', args: [...args, `[${name}]`] })
          console.error('[ERROR]', `[${name}]`, ...args)
        }
      }
    }
  }

  // 基本日志方法
  trace(...args) {
    if (this.isInitialized && this.defaultLogger) {
      this.defaultLogger.trace(...args)
    } else {
      this.pendingLogs.push({ method: 'trace', args })
      console.log('[TRACE]', ...args)
    }
  }

  debug(...args) {
    if (this.isInitialized && this.defaultLogger) {
      this.defaultLogger.debug(...args)
    } else {
      this.pendingLogs.push({ method: 'debug', args })
      console.log('[DEBUG]', ...args)
    }
  }

  info(...args) {
    if (this.isInitialized && this.defaultLogger) {
      this.defaultLogger.info(...args)
    } else {
      this.pendingLogs.push({ method: 'info', args })
      console.info('[INFO]', ...args)
    }
  }

  warn(...args) {
    if (this.isInitialized && this.defaultLogger) {
      this.defaultLogger.warn(...args)
    } else {
      this.pendingLogs.push({ method: 'warn', args })
      console.warn('[WARN]', ...args)
    }
  }

  error(...args) {
    if (this.isInitialized && this.defaultLogger) {
      this.defaultLogger.error(...args)
    } else {
      this.pendingLogs.push({ method: 'error', args })
      console.error('[ERROR]', ...args)
    }
  }

  // 性能日志
  time(label) {
    if (!this.isInitialized) {
      this.init()
    }
    console.time(`⏱️ ${label}`)
  }

  timeEnd(label) {
    if (!this.isInitialized) {
      this.init()
    }
    console.timeEnd(`⏱️ ${label}`)
  }

  // 表格日志
  table(data, columns) {
    if (!this.isInitialized) {
      this.init()
    }
    console.table(data, columns)
  }

  // 分组日志
  group(label, collapsed = false) {
    if (!this.isInitialized) {
      this.init()
    }
    if (collapsed) {
      console.groupCollapsed(`📁 ${label}`)
    } else {
      console.group(`📁 ${label}`)
    }
  }

  groupEnd() {
    console.groupEnd()
  }
}

// 创建默认日志实例
const logger = new Logger()

// 便捷方法
const logTrace = (...args) => logger.trace(...args)
const logDebug = (...args) => logger.debug(...args)
const logInfo = (...args) => logger.info(...args)
const logWarn = (...args) => logger.warn(...args)
const logError = (...args) => logger.error(...args)

// 创建组件日志器
const createLogger = (name) => logger.getLogger(name)

// 性能监控工具
const createPerformanceLogger = (name) => {
  const performanceLogger = logger.getLogger(`Performance-${name}`)

  return {
    startTimer: (operation) => {
      const startTime = performance.now()
      performanceLogger.debug(`⏱️ 开始计时: ${operation}`)
      return {
        end: () => {
          const endTime = performance.now()
          const duration = (endTime - startTime).toFixed(3)
          performanceLogger.info(`⏱️ ${operation} 完成，耗时: ${duration}ms`)
          return parseFloat(duration)
        }
      }
    }
  }
}

// API 请求日志器
const createApiLogger = () => {
  const apiLogger = logger.getLogger('API')

  return {
    request: (method, url, data = null) => {
      apiLogger.info(`📤 发送请求: ${method.toUpperCase()} ${url}`)
      if (data) {
        apiLogger.debug('📦 请求数据:', data)
      }
    },

    response: (method, url, status, data = null, duration = null) => {
      const durationText = duration ? ` | 耗时: ${duration}ms` : ''
      apiLogger.info(`📥 收到响应: ${method.toUpperCase()} ${url} | 状态码: ${status}${durationText}`)
      if (data) {
        apiLogger.debug('📦 响应数据:', data)
      }
    },

    error: (method, url, error, duration = null) => {
      const durationText = duration ? ` | 耗时: ${duration}ms` : ''
      apiLogger.error(`❌ 请求失败: ${method.toUpperCase()} ${url} | 错误: ${error}${durationText}`)
    }
  }
}

export {
  logger,
  logTrace,
  logDebug,
  logInfo,
  logWarn,
  logError,
  createLogger,
  createPerformanceLogger,
  createApiLogger,
  LOG_LEVELS
}

export default logger