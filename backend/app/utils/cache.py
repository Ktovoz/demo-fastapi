"""
简单内存缓存实现
"""
import time
from typing import Any, Optional, Dict


class SimpleCache:
    """简单的内存缓存类"""

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值

        Args:
            key: 缓存键

        Returns:
            缓存值，如果不存在或已过期则返回 None
        """
        if key not in self._cache:
            return None

        cache_item = self._cache[key]
        # 检查是否过期
        if time.time() > cache_item['expires_at']:
            del self._cache[key]
            return None

        return cache_item['value']

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """
        设置缓存值

        Args:
            key: 缓存键
            value: 缓存值
            ttl: 存活时间（秒），默认300秒
        """
        expires_at = time.time() + ttl
        self._cache[key] = {
            'value': value,
            'expires_at': expires_at
        }

    def delete(self, key: str) -> None:
        """
        删除缓存项

        Args:
            key: 缓存键
        """
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        """清空所有缓存"""
        self._cache.clear()


# 创建全局缓存实例
cache = SimpleCache()
