from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from sqlalchemy.orm import Session
from typing import Optional
import json
import time
from datetime import datetime

from ..core.database import get_db
from ..models.operation_log import OperationLog
from ..models.user import User
from ..utils.logger import get_logger

logger = get_logger(__name__)

class AuditLogMiddleware(BaseHTTPMiddleware):
    """审计日志中间件"""

    # 不需要记录日志的路径
    SKIP_PATHS = [
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/favicon.ico",
        "/static"
    ]

    # 不需要记录日志的文件类型
    SKIP_EXTENSIONS = [
        ".css", ".js", ".ico", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".woff", ".woff2"
    ]

    async def dispatch(self, request: Request, call_next):
        # 获取开始时间
        start_time = time.time()

        # 检查是否需要跳过记录
        if self._should_skip_logging(request):
            return await call_next(request)

        logger.debug(f"审计中间件处理请求: {request.method} {request.url.path}")

        # 获取请求信息
        method = request.method
        path = request.url.path
        client_ip = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent", "")

        # 获取当前用户（如果已登录）
        current_user = None
        try:
            # 尝试从请求中获取用户信息
            if hasattr(request.state, 'user'):
                current_user = request.state.user
        except Exception:
            pass

        # 准备记录请求体（仅对非敏感接口）
        request_data = None
        if method in ["POST", "PUT", "PATCH"] and not self._is_sensitive_path(path):
            try:
                # 对于POST/PUT/PATCH请求，尝试获取请求体
                body = await request.body()
                if body:
                    # 限制大小，避免记录大文件
                    if len(body) < 1024 * 10:  # 10KB
                        request_data = json.loads(body.decode())
                    else:
                        request_data = {"message": "请求体过大，已跳过记录"}
            except Exception as e:
                logger.warning(f"获取请求体失败: {str(e)}")

        try:
            # 执行请求
            response = await call_next(request)

            # 计算处理时间
            process_time = round((time.time() - start_time) * 1000, 2)

            # 准备响应数据（仅对成功且非敏感接口）
            response_data = None
            if (response.status_code < 400 and
                not self._is_sensitive_path(path) and
                response.headers.get("content-type", "").startswith("application/json")):
                try:
                    # 获取响应体（仅在开发环境或小响应时）
                    response_body = b""
                    async for chunk in response.body_iterator:
                        response_body += chunk
                        # 限制大小
                        if len(response_body) > 1024 * 5:  # 5KB
                            response_data = {"message": "响应体过大，已跳过记录"}
                            break

                    if response_data is None and response_body:
                        response_data = json.loads(response_body.decode())

                    # 重建响应
                    response = Response(
                        content=response_body,
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        media_type=response.media_type
                    )
                except Exception as e:
                    logger.warning(f"获取响应体失败: {str(e)}")

            # 记录操作日志
            try:
                db_session = next(get_db())
                self._log_operation(
                    db=db_session,
                    user=current_user,
                    method=method,
                    path=path,
                    status_code=response.status_code,
                    ip_address=client_ip,
                    user_agent=user_agent,
                    request_data=request_data,
                    response_data=response_data
                )
                db_session.close()
            except Exception as e:
                logger.error(f"审计日志记录异常: {str(e)}")

            return response

        except Exception as e:
            # 记录异常
            process_time = round((time.time() - start_time) * 1000, 2)

            self._log_operation(
                db=next(get_db()),
                user=current_user,
                method=method,
                path=path,
                status_code=500,
                ip_address=client_ip,
                user_agent=user_agent,
                request_data=request_data,
                response_data=None
            )

            raise

    def _should_skip_logging(self, request: Request) -> bool:
        """判断是否跳过日志记录"""
        path = request.url.path

        # 跳过特定路径
        if any(path.startswith(skip_path) for skip_path in self.SKIP_PATHS):
            return True

        # 跳过静态文件
        if any(path.endswith(ext) for ext in self.SKIP_EXTENSIONS):
            return True

        # 跳过健康检查等系统接口
        if path in ["/", "/health"]:
            return True

        return False

    def _is_sensitive_path(self, path: str) -> bool:
        """判断是否为敏感路径（不记录详细数据）"""
        sensitive_paths = [
            "/auth/login",
            "/auth/register",
            "/auth/refresh",
            "/auth/forgot-password",
            "/users/change-password",
            "/upload",
            "/download"
        ]

        return any(sensitive_path in path for sensitive_path in sensitive_paths)

    def _get_client_ip(self, request: Request) -> str:
        """获取客户端IP地址"""
        # 尝试从各种头部获取真实IP
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip

        # 从客户端地址获取
        if hasattr(request, 'client') and request.client:
            return request.client.host

        return "unknown"

    def _log_operation(
        self,
        db: Session,
        user: Optional[User],
        method: str,
        path: str,
        status_code: int,
        ip_address: str,
        user_agent: str,
        request_data: Optional[dict],
        response_data: Optional[dict]
    ):
        """记录操作日志"""
        try:
            # 确定操作类型和资源
            action, resource = self._parse_action_and_resource(method, path)

            # 生成操作描述
            description = self._generate_description(action, resource, status_code)

            # 提取资源ID
            resource_id = self._extract_resource_id(path)

            # 创建日志记录
            log_entry = OperationLog(
                user_id=user.id if user else None,
                action=action,
                resource=resource,
                resource_id=resource_id,
                description=description,
                ip_address=ip_address,
                user_agent=user_agent,
                request_data=request_data,
                response_data=response_data
            )

            # 保存到数据库
            db.add(log_entry)
            db.commit()

            logger.info(f"记录操作日志: {action} {resource} - 用户: {user.username if user else '匿名'}")

        except Exception as e:
            logger.error(f"记录操作日志失败: {str(e)}")
            try:
                db.rollback()
            except Exception:
                pass

    def _parse_action_and_resource(self, method: str, path: str) -> tuple[str, str]:
        """解析操作类型和资源"""
        # 根据HTTP方法和路径确定操作类型
        path_parts = [part for part in path.split('/') if part]

        if not path_parts:
            return method, "root"

        # 获取主要资源类型
        resource = path_parts[0] if len(path_parts) > 0 else "unknown"

        # 根据方法和路径确定具体操作
        if method == "GET":
            if len(path_parts) > 1 and path_parts[-1].isdigit():
                action = f"查看{resource}"
            else:
                action = f"获取{resource}列表"
        elif method == "POST":
            action = f"创建{resource}"
        elif method == "PUT" or method == "PATCH":
            action = f"更新{resource}"
        elif method == "DELETE":
            action = f"删除{resource}"
        else:
            action = f"{method} {resource}"

        return action, resource

    def _generate_description(
        self,
        action: str,
        resource: str,
        status_code: int
    ) -> str:
        """生成操作描述"""
        if status_code >= 400:
            return f"{action}失败: HTTP {status_code}"
        else:
            return f"{action}成功"

    def _extract_resource_id(self, path: str) -> Optional[int]:
        """从路径中提取资源ID"""
        path_parts = [part for part in path.split('/') if part]

        # 查找最后一个数字部分作为ID
        for part in reversed(path_parts):
            if part.isdigit():
                return int(part)

        return None