# iFlow CLI 项目上下文

## 项目概述

这是一个基于Vue3 + Ant Design Vue前端和FastAPI后端的后台管理系统Demo，采用前后端分离架构，包含完整的用户认证和基础后台管理功能。

## 技术栈

### 后端 (backend/)
- **框架**: FastAPI 0.104.1 - 高性能异步Web框架
- **服务器**: Uvicorn 0.24.0 - ASGI服务器
- **数据库**: SQLite - 轻量级数据库
- **ORM**: SQLAlchemy - Python SQL工具包
- **认证**: JWT + Passlib - 用户认证和密码处理
- **日志**: Loguru 0.7.2 - 简洁高效的日志库
- **环境配置**: Python-dotenv - 环境变量管理

### 前端 (frontend/)
- **框架**: Vue 3.3.11 - 渐进式JavaScript框架
- **UI组件**: Ant Design Vue 4.0.8 - 企业级UI设计语言
- **构建工具**: Vite 5.0.8 - 新一代前端构建工具
- **路由**: Vue Router 4.2.5 - 官方路由管理器
- **状态管理**: Pinia 2.1.7 - Vue的状态管理库
- **HTTP客户端**: Axios 1.6.2 - HTTP请求库
- **日志**: Loglevel 1.8.1 + loglevel-plugin-prefix 0.8.4

## 项目结构

```
D:\code\demo-fastapi\
├── backend/               # FastAPI 后端项目
│   ├── app/              # 应用代码
│   │   ├── main.py       # 应用入口
│   │   ├── database/     # 数据库连接
│   │   ├── models/       # 数据模型
│   │   ├── routers/      # API路由
│   │   ├── schemas/      # Pydantic模式
│   │   └── utils/        # 工具模块
│   │       └── logger.py # 日志系统配置
│   ├── requirements.txt  # Python依赖
│   ├── run.py           # 启动脚本
│   └── start.bat        # Windows启动脚本
├── frontend/              # Vue 3 前端项目
│   ├── src/              # 源代码
│   │   ├── api/          # API接口
│   │   ├── components/   # 公共组件
│   │   ├── views/        # 页面视图
│   │   ├── router/       # 路由配置
│   │   ├── store/        # 状态管理
│   │   └── utils/        # 工具函数
│   │       └── logger.js # 前端日志系统
│   ├── package.json      # 依赖配置
│   └── vite.config.js    # Vite配置
├── doc/                   # 项目文档
└── .github/              # GitHub工作流配置
```

## 开发命令

### 后端开发
```bash
# 进入后端目录
cd backend

# 创建虚拟环境并激活
python -m venv venv
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务
python run.py
# 或
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端开发
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 重要配置

### 后端配置
- **端口**: 8000 (默认)
- **API文档**: http://localhost:8000/docs
- **CORS**: 允许 http://localhost:3000 和 http://127.0.0.1:3000
- **日志系统**: 使用Loguru，支持控制台和文件输出

### 前端配置
- **端口**: 3000 (默认)
- **代理配置**: Vite代理将 /api 请求转发到 http://localhost:8000
- **日志系统**: 使用loglevel，支持本地存储和性能监控

## 日志系统特性

### 后端日志 (backend/app/utils/logger.py)
- 支持多级别日志 (TRACE, DEBUG, INFO, WARN, ERROR)
- 控制台输出带颜色格式化
- 文件日志自动轮转和压缩
- 错误日志单独文件存储
- 函数调用装饰器用于性能监控
- UTF-8编码支持中文日志

### 前端日志 (frontend/src/utils/logger.js)
- 基于loglevel的轻量级日志系统
- 支持本地存储日志到localStorage
- 性能监控工具 (createPerformanceLogger)
- API请求日志记录 (createApiLogger)
- 命名日志器支持模块化日志
- 日志前缀和颜色格式化

## 开发约定

### 代码风格
- Python: 遵循PEP 8规范，使用类型注解
- JavaScript/Vue: 使用ES6+语法，组件化开发
- 中文注释：项目使用中文进行代码注释和文档

### 日志使用
- 后端：使用 `from app.utils.logger import get_logger` 获取日志器
- 前端：使用 `import logger from '@/utils/logger'` 获取日志器
- 日志级别：开发环境使用DEBUG，生产环境使用INFO

### API设计
- RESTful API设计规范
- 统一的响应格式
- JWT认证机制
- 基于角色的权限控制

## 访问地址
- **前端应用**: http://localhost:3000
- **后端API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 注意事项
- 项目使用SQLite数据库，文件位于backend/data/目录
- 前端热重载已启用，修改代码自动刷新
- 后端支持热重载，修改代码自动重启服务
- 日志文件存储在backend/logs/目录
- 默认管理员账号：admin/admin123