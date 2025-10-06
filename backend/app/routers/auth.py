from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, Any

from ..core.database import get_db
from ..models.user import User
from ..models.permission import Permission
from ..utils.security import verify_password, create_access_token, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
from ..utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# 在模块加载时打印路由信息
logger.info("🔧 认证路由模块已加载")
logger.info("📋 认证路由列表:")
logger.info("  - POST /login (表单登录)")
logger.info("  - POST /login-json (JSON登录)")
logger.info("  - POST /register (用户注册)")
logger.info("  - POST /forgot-password (找回密码)")

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """用户登录"""
    logger.info(f"🔐 用户登录接口被调用")
    logger.info(f"📝 登录表单数据: username={form_data.username}")
    logger.debug(f"🔍 完整表单数据: {form_data.__dict__}")
    
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
    logger.info(f"🔐 JSON登录接口被调用")
    logger.info(f"📝 登录数据: email={login_data.get('email')}, remember={login_data.get('remember')}")
    logger.debug(f"🔍 完整登录数据: {login_data}")
    
    email = login_data.get("email")
    password = login_data.get("password")
    remember = login_data.get("remember", False)
    
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱和密码不能为空"
        )
    
    # 查找用户
    logger.info(f"🔍 正在查找用户: email={email}")
    user = db.query(User).filter(User.email == email).first()

    if user:
        logger.info(f"✅ 找到用户: id={user.id}, username={user.username}, email={user.email}")
        logger.debug(f"🔍 用户详情: full_name={user.full_name}, is_active={user.is_active}")
    else:
        logger.warning(f"❌ 登录失败: 邮箱不存在 - {email}")
        logger.debug(f"🔍 数据库中所有用户的邮箱:")
        all_users = db.query(User).all()
        for u in all_users:
            logger.debug(f"  - {u.email} (username: {u.username})")
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

    logger.info(f"🔍 开始获取用户 {user.username} 的角色和权限")
    logger.debug(f"🔍 用户关系: user_roles = {user.user_roles}")

    try:
        # 获取用户角色
        for user_role in user.user_roles:
            role = user_role.role
            user_roles.append(role.name)
            logger.info(f"✅ 找到用户角色: {role.name}")

            # 获取角色权限
            logger.debug(f"🔍 角色 {role.name} 开始获取权限")
            for role_permission in role.role_permissions:
                permission = role_permission.permission
                user_permissions.append(permission.name)
                logger.debug(f"✅ 找到权限: {permission.name} (role_permission_id: {role_permission.id})")

        # 去重
        user_permissions = list(set(user_permissions))

        logger.info(f"📋 用户最终角色: {user_roles}")
        logger.info(f"📋 用户最终权限: {user_permissions}")

    except Exception as e:
        logger.error(f"❌ 获取用户角色权限失败: {str(e)}")
        logger.debug(f"❌ 错误详情: {type(e).__name__}: {str(e)}")
        # 如果获取权限失败，设置默认值
        user_roles = ["user"]
        user_permissions = ["basic"]
        logger.warning(f"⚠️ 使用默认权限: 角色={user_roles}, 权限={user_permissions}")

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

        # 为新用户分配默认角色和权限
        logger.info(f"正在为新用户 {new_user.username} 分配默认角色...")

        # 查找普通用户角色
        from ..models.role import Role
        user_role = db.query(Role).filter(Role.name == "user").first()

        if not user_role:
            logger.warning("未找到普通用户角色，创建默认角色...")
            # 如果不存在，创建默认用户角色
            user_role = Role(
                name="user",
                description="普通用户，拥有基本查看权限"
            )
            db.add(user_role)
            db.commit()
            db.refresh(user_role)

            # 为普通用户角色分配基本权限
            basic_permissions = db.query(Permission).filter(
                Permission.name.in_([
                    "dashboard:view",
                    "users:view",
                    "roles:view"
                ])
            ).all()

            for permission in basic_permissions:
                from ..models.role_permission import RolePermission
                role_permission = RolePermission(
                    role_id=user_role.id,
                    permission_id=permission.id
                )
                db.add(role_permission)

            db.commit()
            logger.info(f"为普通用户角色分配了 {len(basic_permissions)} 个基本权限")

        # 将用户分配到普通用户角色
        from ..models.user_role import UserRole
        user_role_assignment = UserRole(
            user_id=new_user.id,
            role_id=user_role.id
        )
        db.add(user_role_assignment)
        db.commit()

        logger.info(f"✅ 新用户 {new_user.username} 已分配默认角色: {user_role.name}")

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