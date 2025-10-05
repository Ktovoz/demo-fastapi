import sys
import os
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 移除默认的日志处理器
logger.remove()

# 获取日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
LOG_ROTATION = os.getenv("LOG_ROTATION", "10 MB")
LOG_RETENTION = os.getenv("LOG_RETENTION", "7 days")

def setup_logger():
    """设置 loguru 日志记录器"""
    # 确保日志目录存在
    log_dir = Path(LOG_FILE).parent
    log_dir.mkdir(exist_ok=True)

        # 控制台日志处理器
    logger.add(
        sys.stdout,
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        colorize=False,  # 禁用颜色以避免编码问题
        backtrace=True,
        diagnose=True
    )

    # 文件日志处理器
    logger.add(
        LOG_FILE,
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        rotation=LOG_ROTATION,
        retention=LOG_RETENTION,
        compression="zip",
        backtrace=True,
        diagnose=True,
        encoding="utf-8"
    )

    # 错误日志单独文件
    error_log_file = log_dir / "error.log"
    logger.add(
        error_log_file,
        format=LOG_FORMAT,
        level="ERROR",
        rotation=LOG_ROTATION,
        retention=LOG_RETENTION,
        compression="zip",
        backtrace=True,
        diagnose=True,
        encoding="utf-8"
    )

    
    return logger

# 创建全局日志记录器
app_logger = setup_logger()

def get_logger(name: str = None):
    """获取指定名称的日志记录器"""
    if name:
        return logger.bind(name=name)
    return logger

# 日志装饰器
def log_function_call(func_name: str = None):
    """记录关键函数调用的装饰器（仅记录重要操作）"""
    def decorator(func):
        name = func_name or f"{func.__module__}.{func.__name__}"

        async def async_wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"❌ 函数执行失败: {name}, 错误: {str(e)}")
                raise

        def sync_wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"❌ 函数执行失败: {name}, 错误: {str(e)}")
                raise

        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator