# 后台管理Demo系统

一个基于Vue3 + Ant Design Vue前端和FastAPI后端的后台管理系统Demo，包含完整的用户认证和基础后台管理功能。

## 项目概述

本项目是一个前后端分离的后台管理系统Demo，旨在展示现代化的Web应用开发技术栈和最佳实践。系统包含用户认证、权限管理、用户管理、系统监控等核心功能模块，适合作为后台管理系统的学习参考或快速开发模板。

## 技术栈

### 后端技术栈
- **Web框架**: FastAPI - 高性能异步Web框架
- **ASGI服务器**: Uvicorn - ASGI服务器
- **数据库**: SQLite - 轻量级数据库
- **ORM**: SQLAlchemy - Python SQL工具包
- **数据验证**: Pydantic - 类型安全的数据验证
- **身份认证**: JWT + Passlib - 用户认证和密码处理
- **日志系统**: Loguru - 简洁高效的日志库
- **环境配置**: Python-dotenv - 环境变量管理
- **数据库迁移**: Alembic - 数据库版本控制

### 前端技术栈
- **核心框架**: Vue 3 - 渐进式JavaScript框架
- **UI组件库**: Ant Design Vue - 企业级UI设计语言
- **构建工具**: Vite - 新一代前端构建工具
- **路由管理**: Vue Router - 官方路由管理器
- **状态管理**: Pinia - Vue的状态管理库
- **HTTP客户端**: Axios - HTTP请求库
- **日志系统**: Loglevel - 轻量级日志库
- **图标库**: @ant-design/icons-vue - Ant Design图标

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

## 核心功能模块

### 用户认证模块
- **用户注册**: 邮箱/用户名注册
- **用户登录**: 账号密码登录
- **密码重置**: 邮箱验证重置密码
- **JWT认证**: 基于Token的身份认证
- **登录状态**: Token刷新和会话管理

### 用户管理模块
- **用户列表**: 分页查询、搜索过滤
- **用户详情**: 查看用户完整信息
- **用户编辑**: 修改用户信息和权限
- **用户状态**: 启用/禁用用户账号
- **用户删除**: 删除用户账号

### 权限管理模块
- **角色管理**: 创建和管理系统角色
- **权限分配**: 为角色分配不同权限
- **用户角色**: 为用户分配角色
- **权限控制**: 基于角色的访问控制

### 系统监控模块
- **系统概览**: 服务器状态和资源使用情况
- **用户统计**: 用户注册和活跃度统计
- **操作日志**: 用户操作记录和系统日志
- **日志查看**: 分类查看和搜索日志

### 数据管理模块
- **数据概览**: 系统数据统计和可视化
- **数据导入**: Excel/CSV文件导入
- **数据导出**: 数据导出为Excel/CSV
- **数据备份**: 数据库备份和恢复

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