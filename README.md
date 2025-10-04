# Demo FastAPI

一个前后端分离的示例项目，使用 Vue 3 + Ant Design Vue 作为前端，FastAPI 作为后端。

## 项目结构

```
demo-fastapi/
├── frontend/              # Vue 3 前端项目
│   ├── src/
│   │   ├── components/    # Vue 组件
│   │   ├── views/         # 页面视图
│   │   ├── router/        # 路由配置
│   │   ├── store/         # Pinia 状态管理
│   │   ├── utils/         # 工具函数
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 入口文件
│   ├── public/            # 静态资源
│   ├── package.json       # 依赖配置
│   └── vite.config.js     # Vite 配置
├── backend/               # FastAPI 后端项目
│   ├── app/
│   │   ├── main.py        # 应用入口
│   │   ├── models/        # 数据模型
│   │   ├── routers/       # API 路由
│   │   ├── schemas/       # 数据模式
│   │   ├── database/      # 数据库配置
│   │   └── utils/         # 工具函数
│   ├── requirements.txt   # Python 依赖
│   └── .env.example       # 环境变量示例
└── README.md
```

## 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Ant Design Vue** - 企业级 UI 设计语言
- **Vite** - 新一代前端构建工具
- **Vue Router** - Vue.js 官方路由
- **Pinia** - Vue 的状态管理库
- **Axios** - HTTP 请求库

### 后端
- **FastAPI** - 现代、快速的 Web 框架
- **Uvicorn** - ASGI 服务器
- **SQLAlchemy** - SQL 工具包
- **Pydantic** - 数据验证库
- **Python-jose** - JWT 处理
- **Passlib** - 密码处理

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

## 开发指南

### 前端开发
- 前端开发服务器运行在 `http://localhost:3000`
- API 请求通过 Vite 代理到后端 `http://localhost:8000`
- 热重载已启用，修改代码后自动刷新页面

### 后端开发
- 后端服务运行在 `http://localhost:8000`
- API 文档可在 `/docs` 路径查看
- 代码修改后自动重启（开发模式）

### API 端点

#### 基础端点
- `GET /` - 欢迎信息
- `GET /health` - 健康检查

#### API 端点
- `GET /api/` - API 基本信息
- `GET /api/users` - 获取用户列表
- `GET /api/users/{user_id}` - 获取特定用户信息
- `POST /api/echo` - 回显数据

## 项目特性

- ✅ 前后端分离架构
- ✅ RESTful API 设计
- ✅ 响应式 UI 界面
- ✅ 类型安全（TypeScript 风格的数据验证）
- ✅ CORS 跨域支持
- ✅ 热重载开发体验
- ✅ API 自动文档生成
- ✅ 完整的日志系统
  - 后端：Loguru 高性能日志库
  - 前端：Loglevel + 自定义日志工具
  - 支持多级别日志、本地存储、性能监控

## 许可证

MIT License