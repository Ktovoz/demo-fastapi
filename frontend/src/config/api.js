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

// 强制使用HTTPS协议 - 增强检查
if (apiBaseUrl.startsWith('http://')) {
  console.log('🔧 API Config: 检测到HTTP协议，强制转换为HTTPS');
  apiBaseUrl = apiBaseUrl.replace('http://', 'https://');
}

// 再次检查确保使用HTTPS
if (!apiBaseUrl.startsWith('https://')) {
  console.log('🔧 API Config: 缺少协议前缀，添加HTTPS');
  apiBaseUrl = 'https://' + apiBaseUrl;
}

// 确保与前端页面使用相同的域名协议
if (typeof window !== 'undefined' && window.location.protocol === 'https:') {
  // 如果前端使用HTTPS，确保后端也使用HTTPS
  if (apiBaseUrl.startsWith('http://')) {
    console.log('🔧 API Config: 前端使用HTTPS，强制后端也使用HTTPS');
    apiBaseUrl = apiBaseUrl.replace('http://', 'https://');
  }
}

export const API_BASE_URL = apiBaseUrl;

console.log('🔧 API Config: 最终API_BASE_URL:', API_BASE_URL);
console.log('🔧 API Config: URL协议检查:', API_BASE_URL.startsWith('https://') ? 'HTTPS' : 'HTTP');

// 检查是否有其他地方覆盖了配置
if (typeof window !== 'undefined') {
  console.log('🔧 API Config: window.location:', window.location.href);
  console.log('🔧 API Config: 检查环境变量覆盖:', {
    VITE_API_BASE_URL: window.APP_CONFIG?.API_BASE_URL,
    ENV_API_BASE_URL: import.meta.env?.VITE_API_BASE_URL
  });
}

export const API_CONFIG = {
  baseURL: `${API_BASE_URL}/api/`,  // 使用完整的基础URL，确保末尾有斜杠
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};

console.log('🔧 API Config: 最终API_CONFIG:', API_CONFIG);

// 配置加载完成检查 - 增强版本，确保配置正确且使用HTTPS
export const ensureConfigLoaded = () => {
  return new Promise((resolve) => {
    let attempts = 0;
    const maxAttempts = 50; // 最多等待5秒

    const checkConfig = () => {
      attempts++;

      if (window.APP_CONFIG && window.APP_CONFIG.API_BASE_URL) {
        console.log('🔧 API Config: 配置已加载完成');
        console.log('🔧 API Config: API_BASE_URL:', window.APP_CONFIG.API_BASE_URL);

        // 验证配置是否使用HTTPS
        if (window.APP_CONFIG.API_BASE_URL.startsWith('http://')) {
          console.warn('⚠️ API Config: 检测到HTTP配置，强制转换为HTTPS');
          window.APP_CONFIG.API_BASE_URL = window.APP_CONFIG.API_BASE_URL.replace('http://', 'https://');
          console.log('✅ API Config: 已转换为HTTPS:', window.APP_CONFIG.API_BASE_URL);
        }

        console.log('✅ API Config: 配置验证完成，使用HTTPS协议');
        resolve(true);
      } else if (attempts >= maxAttempts) {
        console.error('❌ API Config: 配置加载超时，使用默认HTTPS配置');
        // 设置默认HTTPS配置
        window.APP_CONFIG = {
          API_BASE_URL: 'https://demo-fast-backend.ktovoz.com'
        };
        console.log('🔧 API Config: 已设置默认HTTPS配置:', window.APP_CONFIG);
        resolve(true);
      } else {
        console.log(`🔧 API Config: 等待配置加载... (${attempts}/${maxAttempts})`);
        setTimeout(checkConfig, 100);
      }
    };

    checkConfig();
  });
};