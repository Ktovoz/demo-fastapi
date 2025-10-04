# 🚀 Demo Admin System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Vue 3](https://img.shields.io/badge/Vue%203-3.3.11-4FC08D.svg?style=flat&logo=vue.js)](https://vuejs.org/)
[![Ant Design Vue](https://img.shields.io/badge/Ant%20Design%20Vue-4.0.8-0170FE.svg?style=flat&logo=ant-design)](https://www.antdv.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

一个现代化的前后端分离后台管理系统，采用 **FastAPI + Vue 3 + Ant Design Vue** 技术栈，提供完整的用户认证、权限管理和系统监控功能。

## ✨ 项目亮点

- **🔥 最新技术栈**: FastAPI + Vue 3 + TypeScript 支持
- **🎨 现代化UI**: Ant Design Vue 企业级设计系统
- **🔐 完整认证**: JWT + RBAC 权限管理系统
- **📊 系统监控**: 实时系统状态和日志监控
- **📝 完整日志**: 前后端统一日志系统
- **🚀 开发友好**: 热重载 + 自动API文档 + 代码提示
- **📱 响应式设计**: 支持移动端和桌面端
- **⚡ 高性能**: 异步处理 + 轻量级数据库

## 🎯 核心功能

## 🛠️ 技术架构

### 后端架构 (Python)
| 技术 | 版本 | 用途 |
|------|------|------|
| [FastAPI](https://fastapi.tiangolo.com/) | 0.104.1 | 高性能异步Web框架 |
| [Uvicorn](https://www.uvicorn.org/) | 0.24.0 | ASGI服务器 |
| [SQLAlchemy](https://www.sqlalchemy.org/) | Latest | ORM数据库工具 |
| [Pydantic](https://pydantic-docs.helpmanual.io/) | 2.5.0 | 数据验证和序列化 |
| [JWT](https://jwt.io/) | 3.3.0 | 身份认证 |
| [Passlib](https://passlib.readthedocs.io/) | 1.7.4 | 密码加密 |
| [Loguru](https://loguru.readthedocs.io/) | 0.7.2 | 日志系统 |
| [SQLite](https://www.sqlite.org/) | Built-in | 轻量级数据库 |

### 前端架构 (JavaScript)
| 技术 | 版本 | 用途 |
|------|------|------|
| [Vue 3](https://vuejs.org/) | 3.3.11 | 渐进式JavaScript框架 |
| [Ant Design Vue](https://www.antdv.com/) | 4.0.8 | 企业级UI组件库 |
| [Vite](https://vitejs.dev/) | 5.0.8 | 新一代构建工具 |
| [Vue Router](https://router.vuejs.org/) | 4.2.5 | 路由管理 |
| [Pinia](https://pinia.vuejs.org/) | 2.1.7 | 状态管理 |
| [Axios](https://axios-http.com/) | 1.6.2 | HTTP客户端 |
| [Loglevel](https://github.com/pimterry/loglevel) | 1.8.1 | 前端日志系统 |

## 项目结构

```
demo-fastapi/
├── backend/               # FastAPI 后端项目
│   ├── app/
│   │   ├── core/          # 核心配置
│   │   ├── models/        # 数据模型
│   │   ├── schemas/       # Pydantic模式
│   │   ├── routers/       # API路由
│   │   ├── services/      # 业务逻辑
│   │   ├── utils/         # 工具模块
│   │   └── main.py        # 应用入口
│   ├── alembic/           # 数据库迁移
│   ├── data/              # 数据库文件
│   ├── requirements.txt   # Python 依赖
│   └── .env.example       # 环境变量示例
├── frontend/              # Vue 3 前端项目
│   ├── src/
│   │   ├── api/           # API接口
│   │   ├── components/    # 公共组件
│   │   ├── views/         # 页面视图
│   │   ├── router/        # 路由配置
│   │   ├── store/         # 状态管理
│   │   ├── utils/         # 工具函数
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 入口文件
│   ├── public/            # 静态资源
│   └── package.json       # 依赖配置
└── docs/                  # 项目文档
```

### 🔐 用户认证
- ✅ 邮箱/用户名注册登录
- ✅ JWT Token认证机制
- ✅ 密码加密存储 (bcrypt)
- ✅ Token自动刷新
- ✅ 会话管理

### 👥 用户管理
- ✅ 用户列表分页查询
- ✅ 用户信息编辑
- ✅ 用户状态管理
- ✅ 批量操作支持
- ✅ 高级搜索过滤

### 🔑 权限管理
- ✅ 基于角色的访问控制 (RBAC)
- ✅ 角色创建和管理
- ✅ 权限分配和回收
- ✅ 用户角色关联
- ✅ 动态权限验证

### 📊 系统监控
- ✅ 实时系统状态监控
- ✅ 用户行为统计
- ✅ 操作日志记录
- ✅ 系统性能监控
- ✅ 异常日志追踪

### 📱 响应式界面
- ✅ 移动端适配
- ✅ 主题切换支持
- ✅ 国际化支持
- ✅ 友好的用户交互

## 数据库设计

### 主要数据表
- **users**: 用户基础信息表
- **roles**: 角色信息表
- **permissions**: 权限信息表
- **user_roles**: 用户角色关联表
- **role_permissions**: 角色权限关联表
- **operation_logs**: 操作日志记录表

### 初始化数据
- **默认角色**: 超级管理员、管理员、普通用户
- **默认账号**: admin/admin123 (超级管理员)
- **系统配置**: 基础权限和系统参数

## 快速开始

### 前置要求
- Node.js 16+
- Python 3.8+
- Git

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd demo-fastapi
   ```

2. **启动后端服务**
   ```bash
   cd backend

   # 创建虚拟环境
   python -m venv venv

   # 激活虚拟环境
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate

   # 安装依赖
   pip install -r requirements.txt

   # 复制环境变量文件
   cp .env.example .env

   # 初始化数据库
   python -c "from app.core.database import init_db; init_db()"

   # 启动服务（方式一：使用运行脚本）
   python run.py

   # 或（方式二：直接使用uvicorn）
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   # Windows用户也可以直接双击运行 start.bat
   # Linux/Mac用户可以运行 chmod +x start.sh && ./start.sh
   ```

3. **启动前端服务**
   ```bash
   cd frontend

   # 安装依赖
   npm install

   # 启动开发服务器
   npm run dev
   ```

4. **访问应用**
   - 前端：http://localhost:3000
   - 后端 API 文档：http://localhost:8000/docs

### 默认账号
- **超级管理员**: admin/admin123
- **测试用户**: test/test123

## 开发指南

### 前端开发
- 前端开发服务器运行在 `http://localhost:3000`
- API 请求通过 Vite 代理到后端 `http://localhost:8000`
- 热重载已启用，修改代码后自动刷新页面
- 使用Pinia进行状态管理，Vue Router管理路由

### 后端开发
- 后端服务运行在 `http://localhost:8000`
- API 文档可在 `/docs` 路径查看
- 代码修改后自动重启（开发模式）
- 使用SQLAlchemy ORM操作SQLite数据库
- JWT认证和基于角色的权限控制

### 主要API端点

#### 认证相关
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/refresh` - 刷新Token
- `POST /api/auth/logout` - 用户登出

#### 用户管理
- `GET /api/users` - 获取用户列表
- `GET /api/users/{user_id}` - 获取用户详情
- `PUT /api/users/{user_id}` - 更新用户信息
- `DELETE /api/users/{user_id}` - 删除用户

#### 角色权限
- `GET /api/roles` - 获取角色列表
- `GET /api/permissions` - 获取权限列表
- `POST /api/roles` - 创建角色
- `PUT /api/roles/{role_id}` - 更新角色

#### 系统监控
- `GET /api/dashboard/stats` - 获取系统统计
- `GET /api/logs` - 获取操作日志
- `GET /api/system/info` - 获取系统信息

## 项目特性

- ✅ 前后端分离架构
- ✅ 现代化技术栈 (Vue3 + FastAPI)
- ✅ 完整的用户认证系统
- ✅ 基于角色的权限管理 (RBAC)
- ✅ 响应式 UI 界面
- ✅ RESTful API 设计
- ✅ 类型安全的数据验证
- ✅ SQLite 轻量级数据库
- ✅ 完整的日志系统
  - 后端：Loguru 高性能日志库
  - 前端：Loglevel + 自定义日志工具
  - 支持多级别日志、本地存储、性能监控
- ✅ CORS 跨域支持
- ✅ 热重载开发体验
- ✅ API 自动文档生成
- ✅ 数据库迁移支持 (Alembic)
- ✅ 初始化数据和测试账号

## 许可证

MIT License