// 前端配置文件 - 由 Nginx 提供
console.log('🔧 Config.js: 开始加载配置文件');
console.log('🔧 Config.js: 原始占位符内容', '${VITE_API_BASE_URL}');

window.APP_CONFIG = {
  API_BASE_URL: '${VITE_API_BASE_URL}' || 'http://localhost:8000'
};

console.log('🔧 Config.js: 配置加载完成', window.APP_CONFIG);
console.log('🔧 Config.js: 最终API_BASE_URL:', window.APP_CONFIG.API_BASE_URL);