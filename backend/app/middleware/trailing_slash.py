from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from ..utils.logger import get_logger

logger = get_logger(__name__)

class TrailingSlashMiddleware(BaseHTTPMiddleware):
    """
    全局斜杠处理中间件
    自动处理URL末尾斜杠的不匹配问题，避免307重定向
    """

    def __init__(self, app, redirect_trailing_slash=True):
        super().__init__(app)
        self.redirect_trailing_slash = redirect_trailing_slash

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # 检查是否是API请求
        if not path.startswith("/api"):
            return await call_next(request)

        # 记录原始请求
        original_path = path

        # 处理路径规范化
        normalized_path = self._normalize_path(path)

        # 如果路径被修改了
        if normalized_path != original_path:
            logger.info(f"🔧 路径规范化: {original_path} -> {normalized_path}")

            # 修改请求URL
            request.scope["path"] = normalized_path
            request.scope["raw_path"] = normalized_path.encode()

            # 重建URL对象
            from urllib.parse import urlparse, urlunparse
            parsed_url = urlparse(str(request.url))
            new_url = urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                normalized_path,
                parsed_url.params,
                parsed_url.query,
                parsed_url.fragment
            ))
            request._url = new_url

        response = await call_next(request)
        return response

    def _normalize_path(self, path: str) -> str:
        """
        规范化路径，统一处理斜杠问题
        """
        # 规则1: 确保API路径不以斜杠结尾（除非是根路径）
        if path != "/api/" and path != "/api" and path.endswith("/"):
            return path.rstrip("/")

        # 规则2: 对于特定路径，确保以斜杠结尾
        # 如果有需要特殊处理的路径，可以在这里添加
        # 例如：管理路径等

        return path