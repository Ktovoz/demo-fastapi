// API 配置
console.log('🔧 API Config: 开始初始化API配置');
console.log('🔧 API Config: window.APP_CONFIG:', window.APP_CONFIG);

const config = window.APP_CONFIG || {};

console.log('🔧 API Config: 解析后的config:', config);
console.log('🔧 API Config: config.API_BASE_URL:', config.API_BASE_URL);

export const API_BASE_URL = config.API_BASE_URL || 'http://localhost:8000';

console.log('🔧 API Config: 最终API_BASE_URL:', API_BASE_URL);

export const API_CONFIG = {
  baseURL: `${API_BASE_URL}/api`,  // 使用完整的基础URL
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};

console.log('🔧 API Config: 最终API_CONFIG:', API_CONFIG);