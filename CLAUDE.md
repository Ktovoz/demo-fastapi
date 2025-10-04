# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack admin management demo system built with Vue 3 + Ant Design Vue (frontend) and FastAPI (backend). It implements a complete backend management system with user authentication, role-based access control (RBAC), user management, and system monitoring features.

## Documentation Structure
The project follows a structured documentation approach:
- `doc/开发文档.md`: Overall project architecture and design decisions
- `doc/前端文档.md`: Frontend technology stack and implementation details
- `doc/后端文档.md`: Backend technology stack and implementation details
- `doc/API文档.md`: Unified API interface reference for frontend/backend coordination
- `doc/文档管理规范.md`: Documentation management guidelines and standards

## Development Commands

### Backend Development
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Create and activate virtual environment (Linux/Mac)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables file
cp .env.example .env

# Start development server (option 1 - using run script)
python run.py

# Start development server (option 2 - using uvicorn directly)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Windows users can also double-click start.bat
# Linux/Mac users can run: chmod +x start.sh && ./start.sh
```

### Frontend Development
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc

### Default Credentials
- Super Admin: admin / admin123
- Test User: test / test123

## Architecture Overview

### Backend Architecture (FastAPI)
The backend follows a layered architecture pattern:

- **Core Layer** (`app/core/`): Configuration, security, and database setup
- **Models Layer** (`app/models/`): SQLAlchemy ORM models (User, Role, Permission, etc.)
- **Schemas Layer** (`app/schemas/`): Pydantic models for request/response validation
- **Routers Layer** (`app/routers/`): FastAPI route definitions for API endpoints
- **Services Layer** (`app/services/`): Business logic implementation
- **Utils Layer** (`app/utils/`): Utility functions including logging and security

**Key Design Patterns:**
- Repository pattern for data access through services
- Dependency injection for database sessions and authentication
- JWT-based authentication with refresh tokens
- RBAC (Role-Based Access Control) for authorization
- Comprehensive logging system using Loguru

### Frontend Architecture (Vue 3)
The frontend follows a component-based architecture:

- **Views Layer** (`src/views/`): Page-level components organized by feature
- **Components Layer** (`src/components/`): Reusable UI components
- **API Layer** (`src/api/`): HTTP client abstraction with Axios
- **Store Layer** (`src/store/`): Pinia state management
- **Router Layer** (`src/router/`): Vue Router configuration with guards
- **Utils Layer** (`src/utils/`): Utility functions including logging

**Key Design Patterns:**
- Composition API with `<script setup>` syntax
- Centralized state management with Pinia
- Route guards for authentication and authorization
- API interceptors for request/response handling
- Structured logging system using Loglevel

### Database Design
The system uses SQLite with the following main entities:
- **Users**: User accounts with authentication and profile information
- **Roles**: Role definitions for RBAC system
- **Permissions**: Granular permissions for role assignments
- **User-Role Associations**: Many-to-many relationships
- **Role-Permission Associations**: Many-to-many relationships
- **Operation Logs**: Audit trail for user actions

### Authentication & Authorization Flow
1. User logs in with username/password
2. Backend validates credentials and returns JWT access token + refresh token
3. Frontend stores tokens and includes access token in API requests
4. Backend validates JWT and extracts user information for authorization
5. Role-based permissions are checked for each protected resource
6. Refresh token mechanism for token renewal

## Key Configuration Files

### Backend Configuration
- `backend/app/main.py`: FastAPI application entry point
- `backend/.env`: Environment variables (create from .env.example)
- `backend/requirements.txt`: Python dependencies
- `backend/run.py`: Application startup script with proper path handling

### Frontend Configuration
- `frontend/vite.config.js`: Vite build configuration with proxy setup
- `frontend/package.json`: Node.js dependencies and scripts
- Frontend proxies `/api` requests to `http://localhost:8000`

## Development Guidelines

### Backend Development
- Use Pydantic models for all request/response validation
- Implement proper error handling with HTTP status codes
- Use the logging system (Loguru) for debugging and monitoring
- Follow the repository pattern - business logic goes in services, not in routers
- Use dependency injection for database sessions and other services
- Implement proper authentication checks using the auth utilities

### Frontend Development
- Use Composition API with `<script setup>` syntax consistently
- Implement proper loading states and error handling in API calls
- Use Pinia stores for state management, avoid prop drilling
- Follow the established API client pattern in `src/api/`
- Use the logging system for debugging and monitoring
- Implement proper route guards for protected pages

### Database Operations
- Database is SQLite and located in `backend/data/app.db`
- Database initialization happens automatically on first startup
- Default admin user (admin/admin123) is created during initialization
- Use the service layer for all database operations

### Testing and Quality
- API documentation is automatically generated at `/docs` endpoint
- Use structured logging throughout the application
- Frontend and backend both have comprehensive logging systems
- Environment-specific configurations (development vs production)

## Important Notes

- **Language**: The project uses Chinese language for documentation and UI text
- **Logging**: Both frontend and backend implement comprehensive logging systems
- **Database**: The backend uses SQLite for simplicity, but can be migrated to PostgreSQL/MySQL
- **Ports**: Frontend development server runs on port 3000, backend on port 8000
- **CORS**: Configured to allow frontend-backend communication
- **Authorization**: Complete RBAC authorization system with roles and permissions
- **Initialization**: Database and default admin user are created automatically on first startup
- **Environment**: Copy `.env.example` to `.env` in backend directory before running