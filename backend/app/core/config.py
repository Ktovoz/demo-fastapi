from pydantic_settings import BaseSettings
from typing import Optional, List
import secrets
import os


def get_default_cors_origins() -> List[str]:
    """获取默认的CORS允许源列表"""
    # 开发环境
    dev_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "https://demo-fast.ktovoz.com",  # 生产前端域名（开发时也需要）
        "*"  # 仅开发环境使用
    ]

    # 生产环境 - 只允许特定域名
    prod_origins = [
        "https://demo-fast.ktovoz.com"  # 只允许前端域名
    ]

    # 根据环境返回不同的CORS配置
    import os
    is_dev = os.getenv("DEBUG", "False").lower() == "true"
    return dev_origins if is_dev else prod_origins

class Settings(BaseSettings):
    # 应用基础配置
    APP_NAME: str = "后台管理Demo系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # 安全配置
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7天

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./data/app.db"

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_ROTATION: str = "10 MB"
    LOG_RETENTION: str = "7 days"

    # CORS配置 - 声明类型但不设置默认值
    BACKEND_CORS_ORIGINS: List[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 如果没有通过环境变量或参数设置，则使用默认值
        if not hasattr(self, 'BACKEND_CORS_ORIGINS') or not self.BACKEND_CORS_ORIGINS:
            self.BACKEND_CORS_ORIGINS = get_default_cors_origins()

    # 用户配置
    DEFAULT_ADMIN_USERNAME: str = "admin"
    DEFAULT_ADMIN_PASSWORD: str = "admin123"
    DEFAULT_ADMIN_EMAIL: str = "admin@example.com"

    # 分页配置
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # 允许额外字段

# 创建全局配置实例
settings = Settings()