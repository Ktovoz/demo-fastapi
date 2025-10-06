// 前端配置文件 - 由 Nginx 提供
console.log('🔧 Config.js: 开始加载配置文件');
console.log('🔧 Config.js: 原始占位符内容', '${VITE_API_BASE_URL}');

// 检查占位符是否被替换，如果没有则使用默认值
let apiBaseUrl = '${VITE_API_BASE_URL}';
if (apiBaseUrl.includes('${VITE_API_BASE_URL}') || apiBaseUrl === '${VITE_API_BASE_URL}') {
  console.log('🔧 Config.js: 占位符未被替换，使用默认HTTPS地址');
  apiBaseUrl = 'https://demo-fast-backend.ktovoz.com';
}

window.APP_CONFIG = {
  API_BASE_URL: apiBaseUrl
};

console.log('🔧 Config.js: 配置加载完成', window.APP_CONFIG);
console.log('🔧 Config.js: 最终API_BASE_URL:', window.APP_CONFIG.API_BASE_URL);