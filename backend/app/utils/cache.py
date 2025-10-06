import time
import json
from typing import Any, Optional, Dict, List
from threading import Lock
from datetime import datetime, timedelta
from .logger import get_logger

logger = get_logger(__name__)

class CacheItem:
    """缓存项"""
    def __init__(self, key: str, value: Any, ttl: Optional[int] = None):
        self.key = key
        self.value = value
        self.created_at = time.time()
        self.expires_at = (self.created_at + ttl) if ttl else None
    
    def is_expired(self) -> bool:
        """检查缓存项是否过期"""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def ttl_remaining(self) -> Optional[float]:
        """获取剩余生存时间（秒）"""
        if self.expires_at is None:
            return None
        remaining = self.expires_at - time.time()
        return max(0, remaining) if remaining > 0 else 0

class SimpleCache:
    """简单内存缓存实现"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: Dict[str, CacheItem] = {}
        self.lock = Lock()
        self.hits = 0
        self.misses = 0
        logger.info(f"缓存系统已初始化，最大容量: {max_size}")
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        with self.lock:
            if key in self.cache:
                item = self.cache[key]
                if not item.is_expired():
                    self.hits += 1
                    logger.debug(f"缓存命中: {key}")
                    return item.value
                else:
                    # 删除过期项
                    del self.cache[key]
                    logger.debug(f"缓存过期已删除: {key}")
            
            self.misses += 1
            logger.debug(f"缓存未命中: {key}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存值"""
        with self.lock:
            # 如果缓存已满，删除最旧的项
            if len(self.cache) >= self.max_size:
                # 找到最旧的项并删除
                oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k].created_at)
                del self.cache[oldest_key]
                logger.debug(f"缓存已满，删除最旧项: {oldest_key}")
            
            self.cache[key] = CacheItem(key, value, ttl)
            logger.debug(f"缓存已设置: {key}" + (f" (TTL: {ttl}s)" if ttl else ""))
            return True
    
    def delete(self, key: str) -> bool:
        """删除缓存项"""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                logger.debug(f"缓存已删除: {key}")
                return True
            return False
    
    def clear(self) -> int:
        """清空所有缓存"""
        with self.lock:
            count = len(self.cache)
            self.cache.clear()
            logger.info(f"缓存已清空，共删除 {count} 项")
            return count
    
    def exists(self, key: str) -> bool:
        """检查缓存项是否存在且未过期"""
        with self.lock:
            if key in self.cache:
                item = self.cache[key]
                if not item.is_expired():
                    return True
                else:
                    # 删除过期项
                    del self.cache[key]
            return False
    
    def ttl(self, key: str) -> Optional[float]:
        """获取缓存项的剩余生存时间"""
        with self.lock:
            if key in self.cache:
                item = self.cache[key]
                if not item.is_expired():
                    return item.ttl_remaining()
                else:
                    # 删除过期项
                    del self.cache[key]
            return None
    
    def keys(self) -> List[str]:
        """获取所有未过期的缓存键"""
        with self.lock:
            # 清理过期项
            expired_keys = [key for key, item in self.cache.items() if item.is_expired()]
            for key in expired_keys:
                del self.cache[key]
            
            return list(self.cache.keys())
    
    def stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        with self.lock:
            # 清理过期项
            expired_keys = [key for key, item in self.cache.items() if item.is_expired()]
            for key in expired_keys:
                del self.cache[key]
            
            total_requests = self.hits + self.misses
            hit_rate = self.hits / total_requests if total_requests > 0 else 0
            
            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'hits': self.hits,
                'misses': self.misses,
                'hit_rate': round(hit_rate, 4),
                'expired_items_removed': len(expired_keys)
            }
    
    def cleanup_expired(self) -> int:
        """清理过期的缓存项"""
        with self.lock:
            expired_keys = [key for key, item in self.cache.items() if item.is_expired()]
            for key in expired_keys:
                del self.cache[key]
            
            if expired_keys:
                logger.debug(f"清理了 {len(expired_keys)} 个过期缓存项")
            
            return len(expired_keys)
    
    def cached(self, ttl: Optional[int] = None, key_prefix: str = ""):
        """缓存装饰器"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                # 生成缓存键
                key_parts = [key_prefix, func.__name__]
                if args:
                    key_parts.extend(str(arg) for arg in args)
                if kwargs:
                    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
                
                cache_key = ":".join(key_parts)
                
                # 尝试从缓存获取
                cached_value = self.get(cache_key)
                if cached_value is not None:
                    return cached_value
                
                # 执行函数并缓存结果
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result
            
            return wrapper
        return decorator

# 创建全局缓存实例
cache = SimpleCache()