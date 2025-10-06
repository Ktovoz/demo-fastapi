import time
import json
from typing import Dict, Any, List
from collections import defaultdict, deque
from datetime import datetime, timedelta
from threading import Lock
from .logger import get_logger

logger = get_logger(__name__)

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics = defaultdict(list)  # 存储指标数据
        self.request_stats = defaultdict(lambda: {
            'count': 0,
            'total_time': 0.0,
            'errors': 0,
            'min_time': float('inf'),
            'max_time': 0.0
        })
        self.lock = Lock()
        logger.info("性能监控器已初始化")
    
    def record_request(self, endpoint: str, method: str, duration: float, status_code: int):
        """记录请求性能数据"""
        with self.lock:
            key = f"{method} {endpoint}"
            stats = self.request_stats[key]
            
            stats['count'] += 1
            stats['total_time'] += duration
            stats['min_time'] = min(stats['min_time'], duration)
            stats['max_time'] = max(stats['max_time'], duration)
            
            if status_code >= 400:
                stats['errors'] += 1
            
            # 保存最近的请求数据用于详细分析
            self.metrics[key].append({
                'timestamp': datetime.utcnow().isoformat() + "Z",
                'duration': duration,
                'status_code': status_code
            })
            
            # 限制历史数据大小
            if len(self.metrics[key]) > self.max_history:
                self.metrics[key] = self.metrics[key][-self.max_history:]
            
            logger.debug(f"记录请求性能: {key} - {duration:.3f}s")
    
    def record_function_call(self, function_name: str, duration: float, success: bool = True):
        """记录函数调用性能数据"""
        with self.lock:
            key = f"function:{function_name}"
            stats = self.request_stats[key]
            
            stats['count'] += 1
            stats['total_time'] += duration
            stats['min_time'] = min(stats['min_time'], duration)
            stats['max_time'] = max(stats['max_time'], duration)
            
            if not success:
                stats['errors'] += 1
            
            # 保存最近的函数调用数据
            self.metrics[key].append({
                'timestamp': datetime.utcnow().isoformat() + "Z",
                'duration': duration,
                'success': success
            })
            
            # 限制历史数据大小
            if len(self.metrics[key]) > self.max_history:
                self.metrics[key] = self.metrics[key][-self.max_history:]
            
            logger.debug(f"记录函数性能: {function_name} - {duration:.3f}s")
    
    def get_request_stats(self) -> Dict[str, Any]:
        """获取请求统计信息"""
        with self.lock:
            result = {}
            for endpoint, stats in self.request_stats.items():
                if stats['count'] > 0:
                    avg_time = stats['total_time'] / stats['count']
                    success_rate = (stats['count'] - stats['errors']) / stats['count'] if stats['count'] > 0 else 0
                    
                    result[endpoint] = {
                        'count': stats['count'],
                        'avg_time': round(avg_time, 3),
                        'min_time': round(stats['min_time'], 3),
                        'max_time': round(stats['max_time'], 3),
                        'total_time': round(stats['total_time'], 3),
                        'errors': stats['errors'],
                        'success_rate': round(success_rate, 4)
                    }
            return result
    
    def get_slow_requests(self, threshold: float = 1.0) -> List[Dict[str, Any]]:
        """获取慢请求列表"""
        with self.lock:
            slow_requests = []
            for endpoint, stats in self.request_stats.items():
                if stats['count'] > 0:
                    avg_time = stats['total_time'] / stats['count']
                    if avg_time > threshold:
                        success_rate = (stats['count'] - stats['errors']) / stats['count'] if stats['count'] > 0 else 0
                        slow_requests.append({
                            'endpoint': endpoint,
                            'count': stats['count'],
                            'avg_time': round(avg_time, 3),
                            'min_time': round(stats['min_time'], 3),
                            'max_time': round(stats['max_time'], 3),
                            'errors': stats['errors'],
                            'success_rate': round(success_rate, 4)
                        })
            # 按平均响应时间排序
            slow_requests.sort(key=lambda x: x['avg_time'], reverse=True)
            return slow_requests
    
    def get_recent_metrics(self, endpoint: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """获取最近的指标数据"""
        with self.lock:
            if endpoint:
                # 返回特定端点的最近数据
                data = self.metrics.get(endpoint, [])
                return data[-limit:] if len(data) > limit else data
            else:
                # 返回所有端点的最近数据
                all_data = []
                for key, data in self.metrics.items():
                    for item in data[-10:]:  # 每个端点最多取10个数据点
                        all_data.append({**item, 'endpoint': key})
                # 按时间排序
                all_data.sort(key=lambda x: x['timestamp'], reverse=True)
                return all_data[:limit]
    
    def get_summary(self) -> Dict[str, Any]:
        """获取性能监控摘要"""
        with self.lock:
            total_requests = sum(stats['count'] for stats in self.request_stats.values())
            total_errors = sum(stats['errors'] for stats in self.request_stats.values())
            total_time = sum(stats['total_time'] for stats in self.request_stats.values())
            
            # 计算整体成功率
            success_rate = (total_requests - total_errors) / total_requests if total_requests > 0 else 0
            
            # 计算平均响应时间
            avg_response_time = total_time / total_requests if total_requests > 0 else 0
            
            # 获取最慢的端点
            slow_endpoints = self.get_slow_requests(0.5)  # 超过0.5秒的请求
            
            return {
                'total_requests': total_requests,
                'total_errors': total_errors,
                'success_rate': round(success_rate, 4),
                'avg_response_time': round(avg_response_time, 3),
                'slow_endpoints': slow_endpoints[:10],  # 最多返回10个慢端点
                'active_endpoints': len([s for s in self.request_stats.values() if s['count'] > 0])
            }
    
    def reset_stats(self):
        """重置统计数据"""
        with self.lock:
            self.request_stats.clear()
            self.metrics.clear()
            logger.info("性能统计数据已重置")

# 创建全局性能监控实例
performance_monitor = PerformanceMonitor()

# 性能监控装饰器
def monitor_performance(func_name: str = None):
    """性能监控装饰器"""
    def decorator(func):
        name = func_name or f"{func.__module__}.{func.__name__}"
        
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                performance_monitor.record_function_call(name, duration, True)
                return result
            except Exception as e:
                duration = time.time() - start_time
                performance_monitor.record_function_call(name, duration, False)
                raise
        
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                performance_monitor.record_function_call(name, duration, True)
                return result
            except Exception as e:
                duration = time.time() - start_time
                performance_monitor.record_function_call(name, duration, False)
                raise
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator