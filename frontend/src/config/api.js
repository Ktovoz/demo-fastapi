// API 配置
const config = window.APP_CONFIG || {};

export const API_BASE_URL = config.API_BASE_URL || 'http://localhost:8000';

export const API_CONFIG = {
  baseURL: '/api',  // 使用相对路径，让Vite代理生效
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};