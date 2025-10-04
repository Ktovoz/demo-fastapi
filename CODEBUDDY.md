This file contains essential information for Terminal Assistant Agent to operate effectively in this demo-fastapi repository.

## Project Overview

A full-stack admin system demo with Vue 3 frontend and FastAPI backend, featuring user authentication, role-based access control (RBAC), and system monitoring.

## Development Commands

### Backend (FastAPI)
- **Start development server**: `cd backend && python run.py` (or `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`)
- **Initialize database**: `cd backend && python -c "from app.core.database import init_db; init_db()"`
- **Windows start script**: `cd backend && start.bat`
- **Linux/Mac start script**: `cd backend && chmod +x start.sh && ./start.sh`

### Frontend (Vue 3 + Vite)
- **Start development server**: `cd frontend && npm run dev` (runs on http://localhost:3000)
- **Build for production**: `cd frontend && npm run build`
- **Preview production build**: `cd frontend && npm run preview`

## Architecture

### Backend Structure (`backend/app/`)
- **`main.py`**: Application entry point with CORS, logging middleware, and lifespan management
- **`routers/`**: API endpoints organized by module (currently `api.py` for centralized routing)
- **`models/`**: SQLAlchemy database models
- **`schemas/`**: Pydantic schemas for request/response validation
- **`utils/`**: Utility modules including logging system
- **`database/`**: Database configuration and initialization

### Frontend Structure (`frontend/src/`)
- **`main.js`**: Vue app initialization with Pinia, Vue Router, and Ant Design Vue
- **`router/`**: Vue Router configuration with route guards and logging
- **`store/`**: Pinia state management stores
- **`utils/`**: Utility functions including custom logger system
- **`views/`**: Page components
- **`components/`**: Reusable Vue components

### Key Features
- **Authentication**: JWT-based auth with login, register, refresh, and logout endpoints
- **RBAC**: Role-based permissions with user roles and permission management
- **Logging**: Comprehensive logging system (Loguru backend, Loglevel frontend)
- **API Proxying**: Vite dev server proxies `/api` requests to backend (localhost:8000)
- **Database**: SQLite with Alembic migrations (migration files in `backend/alembic/`)

### API Endpoints
- Auth: `/api/auth/login`, `/api/auth/register`, `/api/auth/refresh`, `/api/auth/logout`
- Users: `/api/users`, `/api/users/{id}` (CRUD operations)
- Roles: `/api/roles` (role management)
- Dashboard: `/api/dashboard/stats` (system statistics)
- Logs: `/api/logs` (operation logs)

### Development Notes
- Backend uses Python 3.8+ with FastAPI, SQLAlchemy, and Pydantic
- Frontend uses Vue 3 with Composition API, Pinia for state management
- UI components from Ant Design Vue
- Database initialized with default admin user: `admin/admin123`
- Frontend development server runs on port 3000 with hot reload
- Backend API runs on port 8000 with auto-generated docs at `/docs`
- Environment variables loaded from `.env` files (use `.env.example` as template)

### Logging System
- Backend: Loguru for structured logging with request/response logging
- Frontend: Custom logger based on Loglevel with prefix formatting and local storage
- Both systems support multiple log levels and performance monitoring

### Testing
- Run backend tests with `pytest` (test files should be in `backend/tests/`)
- Frontend testing setup not yet configured (consider adding Vitest)

This project follows a clean separation of concerns with backend API serving frontend through a proxy during development.