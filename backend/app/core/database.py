from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import os

from .config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={
        "check_same_thread": False,  # SQLite特有配置
    } if settings.DATABASE_URL.startswith("sqlite") else {},
    poolclass=StaticPool if settings.DATABASE_URL.startswith("sqlite") else None,  # SQLite使用静态连接池
    echo=settings.DEBUG  # 开发模式下打印SQL语句
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"数据库会话错误: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """初始化数据库"""
    try:
        # 确保数据目录存在
        os.makedirs(os.path.dirname(settings.DATABASE_URL.replace("sqlite:///", "")), exist_ok=True)

        # 首先导入所有模型以确保它们被正确注册
        from ..models import User, Role, Permission, UserRole, RolePermission, OperationLog
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")

        # 初始化默认数据
        db = SessionLocal()
        try:
            from ..services.init_service import init_default_data
            init_default_data(db)
            logger.info("数据库初始化完成")
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise