// API 配置
const config = window.APP_CONFIG || {};

export const API_BASE_URL = config.API_BASE_URL || 'http://localhost:8000';

export const API_CONFIG = {
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};