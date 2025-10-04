import { defineStore } from 'pinia'
import { createLogger } from '../utils/logger'

// 创建日志器
const logger = createLogger('CounterStore')

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0
  }),
  getters: {
    doubleCount: (state) => {
      logger.debug(`🔢 计算双倍值: ${state.count} * 2 = ${state.count * 2}`)
      return state.count * 2
    }
  },
  actions: {
    increment() {
      const oldValue = this.count
      this.count++
      logger.info(`➕ 计数器增加: ${oldValue} -> ${this.count}`)
    },
    decrement() {
      const oldValue = this.count
      this.count--
      logger.info(`➖ 计数器减少: ${oldValue} -> ${this.count}`)
    },
    reset() {
      const oldValue = this.count
      this.count = 0
      logger.info(`🔄 计数器重置: ${oldValue} -> 0`)
    }
  }
})