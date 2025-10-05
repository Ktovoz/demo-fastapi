from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Dict, Any

from ..core.database import get_db
from ..models.user import User
from ..utils.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..utils.logger import get_logger
from ..services.user_service import UserService, AuthService
from ..core.security import get_current_user
from ..utils.exceptions import service_exception_handler
from ..schemas.base import BaseResponse
from ..schemas.auth import LoginRequest, RegisterRequest, ForgotPasswordRequest, AuthResponse

router = APIRouter()
logger = get_logger(__name__)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


@router.post("/login", response_model=BaseResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    request: Request = None
):
    """用户登录"""
    
    try:
        # 验证用户凭据
        user = AuthService.verify_user_credentials(db, form_data.username, form_data.password)
        if not user:
            logger.warning(f"登录失败: 用户名或密码错误 - {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 更新最后登录时间
        UserService.update_last_login(db, user)
        
        # 获取用户角色和权限
        user_roles, user_permissions = UserService.get_user_roles_and_permissions(db, user)
        
        # 创建访问令牌
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        # 构建响应数据
        user_data = {
            "id": f"USR-{user.id}",
            "name": user.full_name or user.username,
            "email": user.email,
            "role": user_roles[0] if user_roles else "user",  # 主要角色
            "permissions": user_permissions,
            "avatar": user.avatar,
            "lastLogin": user.last_login.isoformat() + "Z" if user.last_login else None
        }
        
        response_data = {
            "token": access_token,
            "expiresIn": ACCESS_TOKEN_EXPIRE_MINUTES,
            "user": user_data
        }

        logger.info(f"用户登录成功: {user.username}")

        # 手动记录登录操作日志（重要的安全事件）
        try:
            ip_address = request.client.host if request and hasattr(request, 'client') else "unknown"
            user_agent = request.headers.get("user-agent", "") if request else ""

            login_log = OperationLog(
                user_id=user.id,
                action="用户登录",
                resource="auth",
                description="用户登录成功",
                ip_address=ip_address,
                user_agent=user_agent,
                request_data={"username": form_data.username},
                response_data={"login_success": True}
            )
            db.add(login_log)
            db.commit()
        except Exception as e:
            logger.warning(f"记录登录日志失败: {str(e)}")
            db.rollback()

        return BaseResponse(
            success=True,
            message="登录成功",
            data=response_data
        )
        
    except Exception as e:
        logger.error(f"用户登录失败: {str(e)}")
        raise service_exception_handler(e)

@router.post("/login-json", response_model=BaseResponse)
async def login_json(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
    request: Request = None
):
    """JSON格式用户登录"""
    
    try:
        email = login_data.email
        password = login_data.password
        remember = login_data.remember or False
        
        # 验证用户凭据
        user = AuthService.verify_user_credentials_by_email(db, email, password)
        if not user:
            logger.warning(f"登录失败: 邮箱或密码错误 - {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 更新最后登录时间
        UserService.update_last_login(db, user)
        
        # 获取用户角色和权限
        user_roles, user_permissions = UserService.get_user_roles_and_permissions(db, user)
        
        # 创建访问令牌
        token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        if remember:
            token_expire_minutes = 7 * 24 * 60  # 7天
        
        access_token_expires = timedelta(minutes=token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        # 构建响应数据
        user_data = {
            "id": f"USR-{user.id}",
            "name": user.full_name or user.username,
            "email": user.email,
            "role": user_roles[0] if user_roles else "user",  # 主要角色
            "permissions": user_permissions,
            "avatar": user.avatar,
            "lastLogin": user.last_login.isoformat() + "Z" if user.last_login else None
        }
        
        response_data = {
            "token": access_token,
            "expiresIn": token_expire_minutes,
            "user": user_data
        }
        
        logger.info(f"用户登录成功: {user.username}")

        # 手动记录登录操作日志（重要的安全事件）
        try:
            ip_address = request.client.host if request and hasattr(request, 'client') else "unknown"
            user_agent = request.headers.get("user-agent", "") if request else ""

            login_log = OperationLog(
                user_id=user.id,
                action="用户登录",
                resource="auth",
                description="用户登录成功(JSON)",
                ip_address=ip_address,
                user_agent=user_agent,
                request_data={"email": login_data.email},
                response_data={"login_success": True}
            )
            db.add(login_log)
            db.commit()
        except Exception as e:
            logger.warning(f"记录登录日志失败: {str(e)}")
            db.rollback()

        return BaseResponse(
            success=True,
            message="登录成功",
            data=response_data
        )
        
    except Exception as e:
        logger.error(f"JSON登录失败: {str(e)}")
        raise service_exception_handler(e)

@router.post("/register", response_model=BaseResponse)
async def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """用户注册"""

    try:
        name = register_data.name
        email = register_data.email
        password = register_data.password

        
        # 检查邮箱是否已存在
        existing_user = UserService.get_user_by_email(db, email)
        if existing_user:
            logger.warning(f"注册失败: 邮箱已存在 - {email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )

        # 检查用户名是否已存在（使用邮箱前缀作为用户名）
        username = email.split("@")[0]
        existing_username = UserService.get_user_by_username(db, username)
        if existing_username:
            # 如果用户名已存在，添加随机数
            import random
            username = f"{username}{random.randint(1000, 9999)}"

        # 创建新用户
        new_user = UserService.create_user(db, username, email, password, name)
        logger.info(f"用户注册成功: {email}")

        # 为新用户分配默认角色
        UserService.assign_default_role(db, new_user)
        logger.info(f"✅ 新用户 {new_user.username} 已分配默认角色")

        return BaseResponse(
            success=True,
            message="注册成功",
            data={"id": f"USR-{new_user.id}"}
        )

    except HTTPException:
        # 重新抛出HTTP异常，不做额外处理
        raise
    except Exception as e:
        logger.error(f"用户注册失败: {str(e)}")
        raise service_exception_handler(e)

@router.post("/forgot-password", response_model=BaseResponse)
async def forgot_password(
    forgot_data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """找回密码"""
    logger.info(f"密码重置请求: {forgot_data.email}")
    
    try:
        email = forgot_data.email
        
        # 查找用户
        user = db.query(User).filter(User.email == email).first()
        if not user:
            # 为了安全，即使用户不存在也返回成功
            logger.info(f"密码重置请求: 邮箱不存在 - {email}")
            return BaseResponse(
                success=True,
                message="如果邮箱存在，重置链接已发送",
                data={"status": "sent"}
            )
        
        # 这里应该实现发送重置邮件的逻辑
        # 由于是演示项目，我们只记录日志
        logger.info(f"密码重置邮件已发送(模拟): {email}")
        
        return BaseResponse(
            success=True,
            message="重置链接已发送",
            data={"status": "sent"}
        )
        
    except Exception as e:
        logger.error(f"找回密码失败: {str(e)}")
        raise service_exception_handler(e)

from ..core.security import get_current_user