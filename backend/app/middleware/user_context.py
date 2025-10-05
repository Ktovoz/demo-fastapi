from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..core.security import verify_token
from ..models.user import User
from ..utils.logger import get_logger

logger = get_logger(__name__)

class UserContextMiddleware(BaseHTTPMiddleware):
    """用户上下文中间件，用于在请求状态中设置当前用户信息"""

    # 不需要用户验证的路径
    SKIP_AUTH_PATHS = [
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/favicon.ico",
        "/static",
        "/api/auth/login",
        "/api/auth/register",
        "/api/auth/forgot-password"
    ]

    async def dispatch(self, request: Request, call_next):
        # 检查是否需要跳过用户验证
        if self._should_skip_auth(request):
            return await call_next(request)

        # 尝试获取用户信息
        current_user = None
        try:
            current_user = await self._get_current_user(request)
        except Exception as e:
            logger.debug(f"获取用户信息失败: {str(e)}")

        # 在请求状态中设置用户信息
        if current_user:
            request.state.user = current_user

        response = await call_next(request)
        return response

    def _should_skip_auth(self, request: Request) -> bool:
        """判断是否跳过用户验证"""
        path = request.url.path
        return any(path.startswith(skip_path) for skip_path in self.SKIP_AUTH_PATHS)

    async def _get_current_user(self, request: Request) -> Optional[User]:
        """获取当前用户"""
        # 从请求头中获取Authorization token
        authorization = request.headers.get("authorization")
        if not authorization:
            return None

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                return None

            # 验证token
            db = next(get_db())
            user = verify_token(token, db, "access")
            return user

        except Exception as e:
            logger.debug(f"Token验证失败: {str(e)}")
            return None