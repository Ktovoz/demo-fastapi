"""
日志管理工具
用于管理应用程序日志文件
"""

import os
import gzip
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LogManager:
    """日志管理器"""

    def __init__(self, log_dir: str = None):
        self.log_dir = Path(log_dir or "logs")
        self.log_dir.mkdir(exist_ok=True)

    def get_log_files(self) -> Dict[str, List[Dict[str, Any]]]:
        """获取所有日志文件信息"""
        log_files = {
            "current": [],  # 当前使用的日志文件
            "archived": [], # 已归档的日志文件
            "compressed": [] # 压缩的日志文件
        }

        for file_path in self.log_dir.rglob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                file_info = {
                    "path": str(file_path),
                    "name": file_path.name,
                    "size_mb": round(stat.st_size / (1024 * 1024), 2),
                    "modified": datetime.fromtimestamp(stat.st_mtime),
                    "size": stat.st_size
                }

                if file_path.suffix == '.gz':
                    log_files["compressed"].append(file_info)
                elif file_path.name.endswith('.log'):
                    log_files["current"].append(file_info)
                else:
                    log_files["archived"].append(file_info)

        # 按修改时间排序
        for category in log_files:
            log_files[category].sort(key=lambda x: x["modified"], reverse=True)

        return log_files

    def cleanup_old_logs(self, days: int = None) -> Dict[str, int]:
        """清理超过指定天数的旧日志文件"""
        retention_days = days or int(settings.LOG_RETENTION.split()[0]) if settings.LOG_RETENTION.isdigit() else 7
        cutoff_date = datetime.now() - timedelta(days=retention_days)

        deleted_count = 0
        deleted_size = 0

        for file_path in self.log_dir.rglob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                file_date = datetime.fromtimestamp(stat.st_mtime)

                if file_date < cutoff_date:
                    try:
                        file_size = file_path.stat().st_size
                        file_path.unlink()
                        deleted_count += 1
                        deleted_size += file_size
                        logger.info(f"删除旧日志文件: {file_path.name}")
                    except Exception as e:
                        logger.error(f"删除日志文件失败 {file_path}: {e}")

        return {
            "deleted_files": deleted_count,
            "freed_size_mb": round(deleted_size / (1024 * 1024), 2)
        }

    def compress_logs(self, max_age_days: int = 1) -> Dict[str, int]:
        """压缩超过指定天数的未压缩日志文件"""
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        compressed_count = 0
        compressed_size = 0

        for file_path in self.log_dir.glob("*.log"):
            if file_path.is_file() and not file_path.name.endswith('.gz'):
                stat = file_path.stat()
                file_date = datetime.fromtimestamp(stat.st_mtime)

                if file_date < cutoff_date:
                    try:
                        # 压缩文件
                        compressed_path = file_path.with_suffix(file_path.suffix + '.gz')
                        with open(file_path, 'rb') as f_in:
                            with gzip.open(compressed_path, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)

                        # 获取文件大小信息
                        original_size = file_path.stat().st_size
                        compressed_size_stat = compressed_path.stat().st_size
                        compressed_size += original_size
                        compressed_count += 1

                        # 删除原文件
                        file_path.unlink()

                        compression_ratio = (1 - compressed_size_stat / original_size) * 100
                        logger.info(f"压缩日志文件: {file_path.name} (压缩率: {compression_ratio:.1f}%)")

                    except Exception as e:
                        logger.error(f"压缩日志文件失败 {file_path}: {e}")

        return {
            "compressed_files": compressed_count,
            "original_size_mb": round(compressed_size / (1024 * 1024), 2)
        }

    def get_log_stats(self) -> Dict[str, Any]:
        """获取日志统计信息"""
        log_files = self.get_log_files()

        total_size = 0
        total_files = 0

        for category, files in log_files.items():
            for file_info in files:
                total_size += file_info["size"]
                total_files += 1

        # 按类型统计
        size_by_type = {}
        for category, files in log_files.items():
            size_by_type[category] = {
                "count": len(files),
                "size_mb": round(sum(f["size"] for f in files) / (1024 * 1024), 2)
            }

        return {
            "total_files": total_files,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "log_directory": str(self.log_dir),
            "by_type": size_by_type,
            "details": log_files
        }

    def rotate_logs_manually(self, max_size_mb: int = 10):
        """手动轮转超过指定大小的日志文件"""
        rotated_count = 0

        for file_path in self.log_dir.glob("*.log"):
            if file_path.is_file():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                if size_mb > max_size_mb:
                    try:
                        # 创建带时间戳的备份文件
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        backup_path = file_path.with_name(
                            f"{file_path.stem}_{timestamp}{file_path.suffix}"
                        )
                        file_path.rename(backup_path)
                        rotated_count += 1
                        logger.info(f"手动轮转日志文件: {file_path.name} -> {backup_path.name}")
                    except Exception as e:
                        logger.error(f"轮转日志文件失败 {file_path}: {e}")

        return {"rotated_files": rotated_count}


def get_log_manager() -> LogManager:
    """获取日志管理器实例"""
    return LogManager()


if __name__ == "__main__":
    # 测试日志管理功能
    manager = get_log_manager()

    # 显示日志统计
    stats = manager.get_log_stats()
    print("📊 日志统计信息:")
    print(f"总文件数: {stats['total_files']}")
    print(f"总大小: {stats['total_size_mb']} MB")
    print(f"日志目录: {stats['log_directory']}")

    for category, info in stats['by_type'].items():
        print(f"{category}: {info['count']} 个文件, {info['size_mb']} MB")