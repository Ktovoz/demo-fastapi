## Project Overview

Full-stack admin system with Vue 3 frontend and FastAPI backend, featuring authentication, RBAC, and monitoring.

## Development Commands

### Backend (FastAPI)
- **Start dev server**: `cd backend && python run.py` (or `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`)
- **Initialize database**: `cd backend && python -c "from app.core.database import init_db; init_db()"`
- **Windows script**: `cd backend && start.bat`
- **Linux/Mac script**: `cd backend && chmod +x start.sh && ./start.sh`

### Frontend (Vue 3 + Vite)  
- **Dev server (real API)**: `cd frontend && npm run dev:real` (port 3000)
- **Dev server (mock API)**: `cd frontend && npm run dev:mock` 
- **Build for production**: `cd frontend && npm run build:real`
- **Preview production**: `cd frontend && npm run preview:real`

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

### Key Endpoints
- Auth: `/api/auth/login`, `/api/auth/register`, `/api/auth/refresh`, `/api/auth/logout`
- Users: `/api/users`, `/api/users/{id}` (CRUD)
- Roles: `/api/roles` (role management)
- Dashboard: `/api/dashboard/stats` (system stats)
- Logs: `/api/logs` (operation logs)

### Default Credentials
- Admin: `admin/admin123`
- Test: `test/test123`

### Development Notes
- Backend: Python 3.8+, FastAPI, SQLAlchemy, Pydantic
- Frontend: Vue 3, Composition API, Pinia, Ant Design Vue
- Frontend proxies `/api` to backend (localhost:8000)
- Backend docs at `/docs` and `/redoc`

### Testing
- Backend: `pytest` (tests in `backend/tests/`)
- Frontend testing not yet configured