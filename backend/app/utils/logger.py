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

# 解析轮转配置，支持多种格式
def parse_rotation(rotation_str: str) -> str:
    """解析日志轮转配置"""
    rotation_str = rotation_str.strip().upper()

    # 支持的格式
    if rotation_str.endswith("MB"):
        return rotation_str.lower()
    elif rotation_str.endswith("KB"):
        return rotation_str.lower()
    elif rotation_str.endswith("GB"):
        return rotation_str.lower()
    elif "HOUR" in rotation_str:
        return rotation_str.lower()
    elif "DAY" in rotation_str:
        return rotation_str.lower()
    elif "WEEK" in rotation_str:
        return rotation_str.lower()
    elif "MONTH" in rotation_str:
        return rotation_str.lower()
    else:
        # 默认按大小轮转
        return rotation_str.lower()

# 解析保留时间配置
def parse_retention(retention_str: str) -> str:
    """解析日志保留时间配置"""
    retention_str = retention_str.strip().upper()

    if retention_str.endswith("DAY"):
        return retention_str.lower()
    elif retention_str.endswith("DAYS"):
        return retention_str.lower().replace("DAYS", " days")
    elif retention_str.endswith("WEEK"):
        return retention_str.lower()
    elif retention_str.endswith("WEEKS"):
        return retention_str.lower().replace("WEEKS", " weeks")
    elif retention_str.endswith("MONTH"):
        return retention_str.lower()
    elif retention_str.endswith("MONTHS"):
        return retention_str.lower().replace("MONTHS", " months")
    elif retention_str.endswith("YEAR"):
        return retention_str.lower()
    elif retention_str.endswith("YEARS"):
        return retention_str.lower().replace("YEARS", " years")
    else:
        return retention_str.lower()

def setup_logger():
    """设置 loguru 日志记录器"""
    # 确保日志目录存在
    log_dir = Path(LOG_FILE).parent
    log_dir.mkdir(exist_ok=True)

    # 解析配置
    rotation_config = parse_rotation(LOG_ROTATION)
    retention_config = parse_retention(LOG_RETENTION)

    print(f"日志配置: 轮转={rotation_config}, 保留={retention_config}")

    # 控制台日志处理器
    logger.add(
        sys.stdout,
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        colorize=False,  # 禁用颜色以避免编码问题
        backtrace=True,
        diagnose=True
    )

    # 主要日志文件处理器
    logger.add(
        LOG_FILE,
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        rotation=rotation_config,
        retention=retention_config,
        compression="zip",
        backtrace=True,
        diagnose=True,
        encoding="utf-8",
        # 添加更多配置选项
        enqueue=True,  # 异步写入
        catch=True,    # 捕获日志写入异常
    )

    # 错误日志单独文件
    error_log_file = log_dir / "error.log"
    logger.add(
        error_log_file,
        format=LOG_FORMAT,
        level="ERROR",
        rotation=rotation_config,
        retention=retention_config,  # 错误日志保留更长时间
        compression="zip",
        backtrace=True,
        diagnose=True,
        encoding="utf-8",
        enqueue=True,
        catch=True,
    )

    # 添加访问日志文件（用于API访问记录）
    access_log_file = log_dir / "access.log"
    logger.add(
        access_log_file,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>API</cyan> - <level>{message}</level>",
        level="INFO",
        rotation="20 MB",  # 访问日志更频繁轮转
        retention="3 days", # 访问日志保留更短时间
        compression="zip",
        filter=lambda record: "access" in record["extra"],
        encoding="utf-8",
        enqueue=True,
        catch=True,
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