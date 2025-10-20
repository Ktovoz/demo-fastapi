"""
日志管理路由
提供日志查看、管理和清理功能
"""

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import Dict, Any, List, Optional
from app.utils.log_manager import get_log_manager
from app.utils.logger import get_logger
from app.core.config import settings

router = APIRouter(prefix="/logs", tags=["日志管理"])
logger = get_logger(__name__)


@router.get("/stats", summary="获取日志统计信息")
async def get_log_statistics():
    """获取日志文件的统计信息"""
    try:
        manager = get_log_manager()
        stats = manager.get_log_stats()
        return {
            "success": True,
            "data": stats,
            "config": {
                "log_level": settings.LOG_LEVEL,
                "log_rotation": settings.LOG_ROTATION,
                "log_retention": settings.LOG_RETENTION,
                "log_file": settings.LOG_FILE
            }
        }
    except Exception as e:
        logger.error(f"获取日志统计失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取日志统计失败: {str(e)}")


@router.get("/files", summary="获取日志文件列表")
async def get_log_files(
    file_type: Optional[str] = Query(None, description="文件类型: current, archived, compressed")
):
    """获取日志文件列表"""
    try:
        manager = get_log_manager()
        all_files = manager.get_log_files()

        if file_type and file_type in all_files:
            return {
                "success": True,
                "data": {
                    file_type: all_files[file_type]
                }
            }
        else:
            return {
                "success": True,
                "data": all_files
            }
    except Exception as e:
        logger.error(f"获取日志文件列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取日志文件列表失败: {str(e)}")


@router.post("/cleanup", summary="清理旧日志文件")
async def cleanup_old_logs(
    background_tasks: BackgroundTasks,
    days: Optional[int] = Query(None, description="保留天数，默认使用配置文件中的设置")
):
    """清理超过指定天数的旧日志文件"""
    try:
        retention_days = days or int(settings.LOG_RETENTION.split()[0]) if settings.LOG_RETENTION.isdigit() else 7

        # 后台任务执行清理
        def cleanup_task():
            try:
                manager = get_log_manager()
                result = manager.cleanup_old_logs(retention_days)
                logger.info(f"日志清理完成: 删除 {result['deleted_files']} 个文件, 释放 {result['freed_size_mb']} MB 空间")
                return result
            except Exception as e:
                logger.error(f"后台日志清理任务失败: {e}")
                return {"error": str(e)}

        background_tasks.add_task(cleanup_task)

        return {
            "success": True,
            "message": f"日志清理任务已启动，将删除超过 {retention_days} 天的日志文件"
        }
    except Exception as e:
        logger.error(f"启动日志清理任务失败: {e}")
        raise HTTPException(status_code=500, detail=f"启动日志清理任务失败: {str(e)}")


@router.post("/compress", summary="压缩日志文件")
async def compress_old_logs(
    background_tasks: BackgroundTasks,
    days: int = Query(1, description="压缩超过指定天数的日志文件")
):
    """压缩超过指定天数的日志文件"""
    try:
        # 后台任务执行压缩
        def compress_task():
            try:
                manager = get_log_manager()
                result = manager.compress_logs(days)
                logger.info(f"日志压缩完成: 压缩 {result['compressed_files']} 个文件, 原始大小 {result['original_size_mb']} MB")
                return result
            except Exception as e:
                logger.error(f"后台日志压缩任务失败: {e}")
                return {"error": str(e)}

        background_tasks.add_task(compress_task)

        return {
            "success": True,
            "message": f"日志压缩任务已启动，将压缩超过 {days} 天的日志文件"
        }
    except Exception as e:
        logger.error(f"启动日志压缩任务失败: {e}")
        raise HTTPException(status_code=500, detail=f"启动日志压缩任务失败: {str(e)}")


@router.post("/rotate", summary="手动轮转日志")
async def rotate_logs_manually(
    background_tasks: BackgroundTasks,
    max_size_mb: int = Query(10, description="超过此大小的日志文件将被轮转")
):
    """手动轮转超过指定大小的日志文件"""
    try:
        # 后台任务执行轮转
        def rotate_task():
            try:
                manager = get_log_manager()
                result = manager.rotate_logs_manually(max_size_mb)
                logger.info(f"日志轮转完成: 轮转 {result['rotated_files']} 个文件")
                return result
            except Exception as e:
                logger.error(f"后台日志轮转任务失败: {e}")
                return {"error": str(e)}

        background_tasks.add_task(rotate_task)

        return {
            "success": True,
            "message": f"日志轮转任务已启动，将轮转超过 {max_size_mb} MB 的日志文件"
        }
    except Exception as e:
        logger.error(f"启动日志轮转任务失败: {e}")
        raise HTTPException(status_code=500, detail=f"启动日志轮转任务失败: {str(e)}")


@router.get("/config", summary="获取日志配置")
async def get_log_config():
    """获取当前日志配置"""
    try:
        return {
            "success": True,
            "data": {
                "log_level": settings.LOG_LEVEL,
                "log_file": settings.LOG_FILE,
                "log_rotation": settings.LOG_ROTATION,
                "log_retention": settings.LOG_RETENTION,
                "supported_rotation_formats": [
                    "10 MB", "50 MB", "100 MB", "1 GB",
                    "1 hour", "1 day", "1 week", "1 month"
                ],
                "supported_retention_formats": [
                    "7 days", "30 days", "90 days",
                    "1 week", "1 month", "1 year"
                ]
            }
        }
    except Exception as e:
        logger.error(f"获取日志配置失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取日志配置失败: {str(e)}")


@router.get("/tail", summary="查看日志末尾内容")
async def tail_log_file(
    filename: str = Query(..., description="日志文件名"),
    lines: int = Query(50, description="显示末尾行数")
):
    """查看指定日志文件的末尾内容"""
    try:
        import subprocess
        import os

        log_file_path = os.path.join("logs", filename)
        if not os.path.exists(log_file_path):
            raise HTTPException(status_code=404, detail=f"日志文件不存在: {filename}")

        # 使用 tail 命令获取文件末尾内容
        try:
            result = subprocess.run(
                ["tail", "-n", str(lines), log_file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            content = result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # 如果 tail 命令不可用，使用 Python 方式读取
            with open(log_file_path, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                content = ''.join(all_lines[-lines:]) if all_lines else ""

        return {
            "success": True,
            "data": {
                "filename": filename,
                "lines": lines,
                "content": content
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查看日志文件失败: {e}")
        raise HTTPException(status_code=500, detail=f"查看日志文件失败: {str(e)}")