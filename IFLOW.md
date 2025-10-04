# iFlow CLI 项目上下文

## 项目概述

这是一个基于Vue3 + Ant Design Vue前端和FastAPI后端的后台管理系统Demo，采用前后端分离架构，包含完整的用户认证、权限管理和基础后台管理功能。项目实现了基于角色的权限控制系统(RBAC)，包含用户、角色、权限的完整管理体系，并配备完善的日志系统和操作记录功能。

## 技术栈

### 后端 (backend/)
- **框架**: FastAPI 0.104.1 - 高性能异步Web框架
- **服务器**: Uvicorn 0.24.0 - ASGI服务器
- **数据库**: SQLite - 轻量级数据库
- **ORM**: SQLAlchemy 2.0.23 - Python SQL工具包
- **认证**: JWT + Passlib - 用户认证和密码处理
- **日志**: Loguru 0.7.2 - 简洁高效的日志库
- **环境配置**: Python-dotenv - 环境变量管理
- **HTTP客户端**: HTTPX 0.25.2 - 异步HTTP客户端
- **数据验证**: Pydantic 2.5.0 - 数据验证和设置管理
- **邮件验证**: Email-validator 2.1.0 - 邮箱格式验证

### 前端 (frontend/)
- **框架**: Vue 3.3.11 - 渐进式JavaScript框架
- **UI组件**: Ant Design Vue 4.0.8 - 企业级UI设计语言
- **图标库**: @ant-design/icons-vue 7.0.1 - Ant Design图标组件
- **构建工具**: Vite 5.0.8 - 新一代前端构建工具
- **路由**: Vue Router 4.2.5 - 官方路由管理器
- **状态管理**: Pinia 2.1.7 - Vue的状态管理库
- **HTTP客户端**: Axios 1.6.2 - HTTP请求库
- **日志**: Loglevel 1.8.1 + loglevel-plugin-prefix 0.8.4
- **环境变量**: Cross-env 7.0.3 - 跨平台环境变量设置

## 项目结构

```
D:\code\demo-fastapi\
├── backend/               # FastAPI 后端项目
│   ├── app/              # 应用代码
│   │   ├── core/         # 核心模块
│   │   │   ├── config.py # 配置管理
│   │   │   ├── database.py # 数据库连接
│   │   │   └── security.py # 安全相关
│   │   ├── models/       # 数据模型
│   │   │   ├── base.py   # 基础模型
│   │   │   ├── user.py   # 用户模型
│   │   │   ├── role.py   # 角色模型
│   │   │   ├── permission.py # 权限模型
│   │   │   ├── user_role.py # 用户角色关联
│   │   │   ├── role_permission.py # 角色权限关联
│   │   │   └── operation_log.py # 操作日志模型
│   │   ├── routers/      # API路由
│   │   │   └── api.py    # API路由定义
│   │   ├── schemas/      # Pydantic模式
│   │   ├── services/     # 业务服务
│   │   ├── utils/        # 工具模块
│   │   │   ├── logger.py # 日志系统配置
│   │   │   └── security.py # 安全工具
│   │   └── main.py       # 应用入口
│   ├── alembic/          # 数据库迁移
│   ├── data/             # 数据库文件
│   ├── logs/             # 日志文件
│   ├── tests/            # 测试文件
│   ├── uploads/          # 上传文件
│   ├── requirements.txt  # Python依赖
│   ├── run.py           # 启动脚本
│   ├── start.bat        # Windows启动脚本
│   └── start.sh         # Linux启动脚本
├── frontend/              # Vue 3 前端项目
│   ├── src/              # 源代码
│   │   ├── api/          # API接口
│   │   │   ├── auth.js   # 认证接口
│   │   │   ├── user.js   # 用户接口
│   │   │   ├── role.js   # 角色接口
│   │   │   ├── admin.js  # 管理员接口
│   │   │   ├── dashboard.js # 仪表板接口
│   │   │   └── system.js # 系统接口
│   │   ├── components/   # 公共组件
│   │   │   ├── layout/   # 布局组件
│   │   │   ├── common/   # 通用组件
│   │   │   └── business/ # 业务组件
│   │   ├── views/        # 页面视图
│   │   │   ├── auth/     # 认证页面
│   │   │   ├── users/    # 用户管理
│   │   │   ├── roles/    # 角色管理
│   │   │   ├── system/   # 系统管理
│   │   │   ├── dashboard/ # 仪表板
│   │   │   ├── profile/  # 个人资料
│   │   │   └── error/    # 错误页面
│   │   ├── router/       # 路由配置
│   │   ├── store/        # 状态管理
│   │   ├── utils/        # 工具函数
│   │   │   ├── logger.js # 前端日志系统
│   │   │   └── api.js    # API工具
│   │   ├── config/       # 配置文件
│   │   ├── layouts/      # 布局模板
│   │   ├── mock/         # 模拟数据
│   │   ├── App.vue       # 根组件
│   │   └── main.js       # 应用入口
│   ├── public/           # 静态资源
│   ├── dist/             # 构建输出
│   ├── package.json      # 依赖配置
│   └── vite.config.js    # Vite配置
├── doc/                   # 项目文档
│   ├── 开发文档.md
│   ├── 前端文档.md
│   ├── 后端文档.md
│   ├── API文档.md
│   └── 文档管理规范.md
├── .github/              # GitHub工作流配置
│   └── workflows/
│       └── docker-image.yml
└── src/                  # 项目资源文件
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

# 启动服务 (方式1: 使用启动脚本)
python run.py

# 启动服务 (方式2: 直接使用uvicorn)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Windows快速启动
start.bat
```

### 前端开发
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器 (真实API)
npm run dev

# 启动开发服务器 (模拟数据)
npm run dev:mock

# 构建生产版本 (真实API)
npm run build

# 构建生产版本 (模拟数据)
npm run build:mock

# 预览构建结果
npm run preview
```

## 重要配置

### 后端配置
- **端口**: 8000 (默认)
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **CORS**: 允许 http://localhost:3000, http://localhost:5173, http://127.0.0.1:3000
- **日志系统**: 使用Loguru，支持控制台和文件输出
- **数据库**: SQLite，文件位于 backend/data/app.db
- **认证方式**: JWT Token
- **环境配置**: 支持 .env 文件配置

### 前端配置
- **端口**: 3000 (开发), 4173 (预览)
- **代理配置**: Vite代理将 /api 请求转发到 http://localhost:8000
- **日志系统**: 使用loglevel，支持本地存储和性能监控
- **构建优化**: 代码分割和chunk优化
- **Mock数据**: 支持模拟数据和真实API切换

## 核心功能模块

### 用户认证系统
- JWT Token认证
- 登录/注册/密码重置
- 用户会话管理
- 权限验证中间件

### 权限管理系统
- 基于角色的权限控制(RBAC)
- 用户-角色-权限三级关联
- 动态权限验证
- 权限继承机制

### 操作日志系统
- 用户操作记录
- 系统日志管理
- 日志级别控制
- 日志文件轮转

### 前端页面模块
- **仪表板**: 系统概览和数据统计
- **用户管理**: 用户CRUD操作和角色分配
- **角色管理**: 角色权限配置和管理
- **系统管理**: 系统设置和日志查看
- **个人资料**: 用户信息管理

## 日志系统特性

### 后端日志 (backend/app/utils/logger.py)
- 支持多级别日志 (TRACE, DEBUG, INFO, WARN, ERROR)
- 控制台输出带颜色格式化
- 文件日志自动轮转和压缩
- 错误日志单独文件存储
- 函数调用装饰器用于性能监控
- UTF-8编码支持中文日志
- 请求响应日志中间件

### 前端日志 (frontend/src/utils/logger.js)
- 基于loglevel的轻量级日志系统
- 支持本地存储日志到localStorage
- 性能监控工具 (createPerformanceLogger)
- API请求日志记录 (createApiLogger)
- 命名日志器支持模块化日志
- 日志前缀和颜色格式化
- 待处理日志队列机制

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
- 错误处理和异常捕获

### 数据库设计
- SQLAlchemy ORM模型
- 基础模型类提供通用字段
- 关联关系定义
- 数据库迁移支持

## 访问地址
- **前端应用**: http://localhost:3000
- **后端API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **API根路径**: http://localhost:8000/api

## 环境变量配置

### 后端环境变量 (.env)
```env
# 应用配置
APP_NAME=后台管理Demo系统
APP_VERSION=1.0.0
DEBUG=true

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 安全配置
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 数据库配置
DATABASE_URL=sqlite:///./data/app.db

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### 前端环境变量
```env
# API配置
VITE_API_BASE_URL=http://localhost:8000/api
VITE_USE_MOCK=false
```

## 注意事项
- 项目使用SQLite数据库，文件位于backend/data/目录
- 前端热重载已启用，修改代码自动刷新
- 后端支持热重载，修改代码自动重启服务
- 日志文件存储在backend/logs/目录
- 默认管理员账号：admin/admin123
- 前端支持Mock数据和真实API切换
- 项目包含完整的RBAC权限系统
- 所有API请求都有日志记录
- 支持Docker容器化部署