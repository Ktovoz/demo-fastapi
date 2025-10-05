from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, Any

from ..core.database import get_db
from ..models.user import User
from ..utils.security import verify_password, create_access_token, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
from ..utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """用户登录"""
    logger.info(f"用户登录尝试: {form_data.username}")
    
    # 查找用户
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        logger.warning(f"登录失败: 用户不存在 - {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 验证密码
    if not verify_password(form_data.password, user.password_hash):
        logger.warning(f"登录失败: 密码错误 - {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    db.commit()
    
    # 获取用户角色和权限
    user_roles = []
    user_permissions = []
    
    try:
        # 获取用户角色
        for user_role in user.user_roles:
            role = user_role.role
            user_roles.append(role.name)
            
            # 获取角色权限
            for role_permission in role.role_permissions:
                permission = role_permission.permission
                user_permissions.append(permission.name)
        
        # 去重
        user_permissions = list(set(user_permissions))
        
    except Exception as e:
        logger.error(f"获取用户角色权限失败: {str(e)}")
        # 如果获取权限失败，设置默认值
        user_roles = ["user"]
        user_permissions = ["basic"]
    
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
    logger.debug(f"用户数据: {user_data}")
    
    return response_data

@router.post("/login-json")
async def login_json(
    login_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """JSON格式用户登录"""
    logger.info(f"用户登录尝试(JSON): {login_data.get('email')}")
    
    email = login_data.get("email")
    password = login_data.get("password")
    remember = login_data.get("remember", False)
    
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱和密码不能为空"
        )
    
    # 查找用户
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning(f"登录失败: 邮箱不存在 - {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 验证密码
    if not verify_password(password, user.password_hash):
        logger.warning(f"登录失败: 密码错误 - {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    db.commit()
    
    # 获取用户角色和权限
    user_roles = []
    user_permissions = []
    
    try:
        # 获取用户角色
        for user_role in user.user_roles:
            role = user_role.role
            user_roles.append(role.name)
            
            # 获取角色权限
            for role_permission in role.role_permissions:
                permission = role_permission.permission
                user_permissions.append(permission.name)
        
        # 去重
        user_permissions = list(set(user_permissions))
        
    except Exception as e:
        logger.error(f"获取用户角色权限失败: {str(e)}")
        # 如果获取权限失败，设置默认值
        user_roles = ["user"]
        user_permissions = ["basic"]
    
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
    
    logger.info(f"用户登录成功(JSON): {user.username}")
    logger.debug(f"用户数据: {user_data}")
    
    return response_data

@router.post("/register")
async def register(
    register_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """用户注册"""
    logger.info(f"用户注册尝试: {register_data.get('email')}")
    
    name = register_data.get("name")
    email = register_data.get("email")
    password = register_data.get("password")
    
    # 验证必填字段
    if not name or not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="姓名、邮箱和密码不能为空"
        )
    
    # 检查邮箱是否已存在
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        logger.warning(f"注册失败: 邮箱已存在 - {email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 检查用户名是否已存在（使用邮箱前缀作为用户名）
    username = email.split("@")[0]
    existing_username = db.query(User).filter(User.username == username).first()
    if existing_username:
        # 如果用户名已存在，添加随机数
        import random
        username = f"{username}{random.randint(1000, 9999)}"
    
    try:
        # 创建新用户
        hashed_password = get_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            full_name=name
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"用户注册成功: {email}")
        
        return {"id": f"USR-{new_user.id}"}
        
    except Exception as e:
        logger.error(f"用户注册失败: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册失败，请稍后再试"
        )

@router.post("/forgot-password")
async def forgot_password(
    forgot_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """找回密码"""
    logger.info(f"密码重置请求: {forgot_data.get('email')}")
    
    email = forgot_data.get("email")
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱不能为空"
        )
    
    # 查找用户
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # 为了安全，即使用户不存在也返回成功
        logger.info(f"密码重置请求: 邮箱不存在 - {email}")
        return {"status": "sent"}
    
    # 这里应该实现发送重置邮件的逻辑
    # 由于是演示项目，我们只记录日志
    logger.info(f"密码重置邮件已发送(模拟): {email}")
    
    return {"status": "sent"}

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        from ..utils.security import verify_token
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user