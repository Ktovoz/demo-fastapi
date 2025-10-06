// API 配置
console.log('🔧 API Config: 开始初始化API配置');
console.log('🔧 API Config: window.APP_CONFIG:', window.APP_CONFIG);

const config = window.APP_CONFIG || {};

console.log('🔧 API Config: 解析后的config:', config);
console.log('🔧 API Config: config.API_BASE_URL:', config.API_BASE_URL);

// 检查API_BASE_URL是否是占位符，如果是则使用默认值
let apiBaseUrl = config.API_BASE_URL || 'https://demo-fast-backend.ktovoz.com';
if (apiBaseUrl.includes('${VITE_API_BASE_URL}') || apiBaseUrl === '${VITE_API_BASE_URL}') {
  console.log('🔧 API Config: 检测到未替换的占位符，使用默认值');
  apiBaseUrl = 'https://demo-fast-backend.ktovoz.com';
}

export const API_BASE_URL = apiBaseUrl;

console.log('🔧 API Config: 最终API_BASE_URL:', API_BASE_URL);
console.log('🔧 API Config: URL协议检查:', API_BASE_URL.startsWith('https://') ? 'HTTPS' : 'HTTP');

export const API_CONFIG = {
  baseURL: `${API_BASE_URL}/api`,  // 使用完整的基础URL
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};

console.log('🔧 API Config: 最终API_CONFIG:', API_CONFIG);