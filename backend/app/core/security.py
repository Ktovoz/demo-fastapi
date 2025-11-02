from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .config import settings
from ..models.user import User
from ..core.database import get_db
from ..utils.logger import get_logger

logger = get_logger(__name__)

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login-json")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"密码验证失败: {e}")
        return False

def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"密码哈希生成失败: {e}")
        raise

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    logger.info(f"🏗️ 开始创建访问令牌，原始数据: {data}")

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire, "type": "access"})
    logger.info(f"📦 准备编码的JWT数据: {to_encode}")

    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        logger.info(f"✅ 访问令牌创建成功，前缀: {encoded_jwt[:30]}..." if len(encoded_jwt) > 30 else f"令牌: {encoded_jwt}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"创建访问令牌失败: {e}")
        raise

def create_refresh_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """创建刷新令牌"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh"
    }

    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"创建刷新令牌失败: {e}")
        raise

def verify_token(token: str, db: Session, token_type: str = "access") -> Optional[User]:
    """验证令牌"""
    try:
        logger.info(f"🔍 开始验证令牌，类型: {token_type}")
        logger.info(f"🔑 令牌前缀: {token[:30]}..." if len(token) > 30 else f"令牌: {token}")

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        logger.info(f"✅ JWT解码成功，payload: {payload}")

        # 检查令牌类型
        token_type_in_payload = payload.get("type")
        logger.info(f"🔍 令牌中的类型: {token_type_in_payload}, 期望类型: {token_type}")

        # 兼容旧令牌：如果没有type字段，假设是access令牌
        if token_type_in_payload is None:
            logger.info(f"⚠️ 令牌缺少type字段，假设为旧版本访问令牌")
            token_type_in_payload = "access"
            # 更新payload以保持一致性
            payload["type"] = "access"

        if token_type_in_payload != token_type:
            logger.warning(f"❌ 令牌类型不匹配: 期望{token_type}, 实际{token_type_in_payload}")
            logger.warning(f"📄 完整payload内容: {payload}")
            return None

        user_id: str = payload.get("sub")
        if user_id is None:
            logger.warning("❌ 令牌中缺少用户ID")
            logger.warning(f"📄 payload内容: {payload}")
            return None

        logger.info(f"👤 令牌中的用户标识: {user_id}")

        # 兼容旧令牌：用户标识可能是ID或用户名
        user = None
        try:
            # 首先尝试作为ID查找
            user = db.query(User).filter(User.id == int(user_id)).first()
            if user:
                logger.info(f"✅ 通过ID找到用户: {user.username}")
        except ValueError:
            # 如果不是数字，尝试作为用户名查找
            user = db.query(User).filter(User.username == user_id).first()
            if user:
                logger.info(f"✅ 通过用户名找到用户: {user.username}")

        if user is None:
            logger.warning(f"❌ 用户不存在: {user_id}")
            return None

        if not user.is_active:
            logger.warning(f"用户已被禁用: {user_id}")
            return None

        logger.info(f"✅ 令牌验证成功，用户: {user.username}, is_superuser: {user.is_superuser}")
        return user
    except JWTError as e:
        logger.warning(f"JWT令牌验证失败: {e}")
        logger.warning(f"失败原因: {type(e).__name__}")
        logger.warning(f"失败的令牌: {token[:30]}..." if len(token) > 30 else f"令牌: {token}")
        logger.warning(f"使用的密钥算法: {settings.ALGORITHM}")
        logger.warning(f"密钥前缀: {settings.SECRET_KEY[:10]}..." if len(settings.SECRET_KEY) > 10 else f"密钥: {settings.SECRET_KEY}")
        return None
    except Exception as e:
        logger.error(f"令牌验证过程出错: {e}")
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"失败的令牌: {token[:30]}..." if len(token) > 30 else f"令牌: {token}")
        return None

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = verify_token(token, db, "access")
    if user is None:
        raise credentials_exception

    return user