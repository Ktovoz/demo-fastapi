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

## 🤝 贡献指南

我们欢迎社区贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目开发。

### 🐛 报告问题
如果您发现了bug，请在 [Issues](https://github.com/your-username/demo-fastapi/issues) 页面提交问题报告。

### 💡 功能建议
有新功能想法？欢迎提交 [Feature Request](https://github.com/your-username/demo-fastapi/issues/new?template=feature_request.md)。

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源协议发布。

## ⭐ Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=your-username/demo-fastapi&type=Date)](https://star-history.com/#your-username/demo-fastapi&Date)

---

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 高性能Web框架
- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架  
- [Ant Design Vue](https://www.antdv.com/) - 企业级UI设计语言
- [Vite](https://vitejs.dev/) - 极速构建工具

**如果觉得项目有帮助，请给个 ⭐️ Star 支持一下！**

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

## 🚀 快速开始

### 📋 环境要求
- **Node.js**: 16.0 或更高版本
- **Python**: 3.8 或更高版本  
- **Git**: 最新版本

### ⚡ 一键启动

#### 1. 克隆项目
```bash
git clone https://github.com/your-username/demo-fastapi.git
cd demo-fastapi
```

#### 2. 启动后端 (FastAPI)
```bash
cd backend

# Windows 用户
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py

# Linux/Mac 用户  
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

#### 3. 启动前端 (Vue 3)
```bash
cd frontend
npm install
npm run dev
```

### 🌐 访问应用
- **前端界面**: http://localhost:3000
- **API文档**: http://localhost:8000/docs  
- **备用API**: http://localhost:8000/redoc

### 🔑 默认账号
| 角色 | 用户名 | 密码 | 权限 |
|------|--------|------|------|
| 超级管理员 | `admin` | `admin123` | 全部权限 |
| 测试用户 | `test` | `test123` | 基础权限 |

## 💻 开发指南

### 🔧 环境配置
项目支持开发环境和生产环境配置：

#### 开发环境
```bash
# 后端 - 自动热重载
python run.py

# 前端 - 热更新开发服务器  
npm run dev
```

#### 生产环境
```bash
# 构建前端
npm run build

# 生产环境启动后端
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 📚 API文档
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### 🎯 核心API端点

#### 🔐 认证模块
```http
POST /api/auth/login     # 用户登录
POST /api/auth/register  # 用户注册  
POST /api/auth/refresh   # Token刷新
POST /api/auth/logout    # 用户登出
```

#### 👥 用户管理
```http
GET    /api/users           # 获取用户列表
GET    /api/users/{id}      # 获取用户详情
PUT    /api/users/{id}      # 更新用户信息
DELETE /api/users/{id}      # 删除用户
```

#### 🔑 权限管理
```http
GET    /api/roles           # 获取角色列表
POST   /api/roles           # 创建角色
PUT    /api/roles/{id}      # 更新角色
GET    /api/permissions     # 获取权限列表
```

#### 📊 系统监控
```http
GET /api/dashboard/stats   # 系统统计
GET /api/logs              # 操作日志
GET /api/system/info       # 系统信息
```

### 📝 日志系统

#### 后端日志 (Loguru)
```python
from app.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("用户登录成功", user_id=user.id)
```

#### 前端日志 (Loglevel)
```javascript
import logger from '@/utils/logger'

logger.info('组件初始化完成')
const apiLogger = logger.createApiLogger()
apiLogger.request('GET', '/api/users')
```

## 📸 界面预览

### 🎨 登录页面
*现代化的登录界面，支持记住密码和自动登录*

### 📊 仪表板
*数据可视化面板，实时展示系统状态和用户统计*

### 👥 用户管理
*完整的用户CRUD操作，支持批量处理和高级搜索*

### 🔑 权限管理  
*基于角色的权限控制系统，灵活的权限分配*

### 📋 系统日志
*详细的操作日志记录，支持分类查看和搜索过滤*

## 🏗️ 项目结构
```
demo-fastapi/
├── backend/               # 🚀 FastAPI 后端
│   ├── app/              # 应用核心
│   │   ├── main.py       # 应用入口
│   │   ├── routers/      # API路由
│   │   ├── models/       # 数据模型
│   │   ├── schemas/      # 数据验证
│   │   └── utils/        # 工具函数
│   ├── requirements.txt  # Python依赖
│   └── run.py           # 启动脚本
├── frontend/              # 🎨 Vue 3 前端
│   ├── src/              # 源代码
│   │   ├── views/        # 页面组件
│   │   ├── components/   # 公共组件
│   │   ├── api/          # API接口
│   │   └── utils/        # 工具函数
│   ├── package.json      # 依赖配置
│   └── vite.config.js    # 构建配置
└── doc/                  # 📚 项目文档
```

## 许可证

MIT License