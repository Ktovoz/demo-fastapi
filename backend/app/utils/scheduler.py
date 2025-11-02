import asyncio
from datetime import datetime, time, timedelta
from typing import Callable, Dict, Any

from ..core.database import SessionLocal
from ..utils.logger import get_logger
from ..services.system_init_service import SystemInitService

logger = get_logger(__name__)

class SystemScheduler:
    """系统定时任务调度器"""

    def __init__(self):
        self.is_running = False
        self.tasks: Dict[str, Callable] = {}
        self._task = None

    def add_task(self, name: str, task_func: Callable):
        """添加定时任务"""
        self.tasks[name] = task_func
        logger.info(f"添加定时任务: {name}")

    def remove_task(self, name: str):
        """移除定时任务"""
        if name in self.tasks:
            del self.tasks[name]
            logger.info(f"移除定时任务: {name}")

    async def start(self):
        """启动调度器"""
        if self.is_running:
            logger.warning("调度器已经在运行中")
            return

        self.is_running = True
        self._task = asyncio.create_task(self._run_scheduler())
        logger.info("系统调度器已启动")

    async def stop(self):
        """停止调度器"""
        if not self.is_running:
            return

        self.is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        logger.info("系统调度器已停止")

    async def _run_scheduler(self):
        """运行调度器主循环"""
        logger.info("调度器开始运行")

        while self.is_running:
            try:
                # 获取当前时间
                now = datetime.utcnow()

                # 检查是否接近下一个执行时间（提前1分钟检查）
                next_run = now.replace(hour=0, minute=0, second=0, microsecond=0)
                if now.hour >= 0:
                    next_run = next_run + timedelta(days=1)

                time_to_wait = (next_run - now).total_seconds()

                # 如果距离执行时间超过1分钟，等待到前1分钟
                if time_to_wait > 60:
                    wait_time = time_to_wait - 60
                    logger.debug(f"距离下次执行还有 {wait_time/3600:.1f} 小时")
                    await asyncio.sleep(wait_time)
                    continue

                # 在执行时间前1分钟内，每10秒检查一次
                while time_to_wait > 0 and self.is_running:
                    await asyncio.sleep(min(10, time_to_wait))
                    now = datetime.utcnow()
                    time_to_wait = (next_run - now).total_seconds()

                if self.is_running and time_to_wait <= 0:
                    # 执行所有任务
                    logger.info("开始执行定时任务")
                    for task_name, task_func in self.tasks.items():
                        try:
                            logger.info(f"执行任务: {task_name}")
                            result = await task_func()
                            logger.info(f"任务 {task_name} 执行完成: {result}")
                        except Exception as e:
                            logger.error(f"任务 {task_name} 执行失败: {str(e)}")

                    logger.info("所有定时任务执行完成")

            except Exception as e:
                logger.error(f"调度器运行异常: {str(e)}")
                await asyncio.sleep(60)  # 异常后等待1分钟再继续

    def get_status(self) -> Dict[str, Any]:
        """获取调度器状态"""
        return {
            "is_running": self.is_running,
            "tasks": list(self.tasks.keys()),
            "next_run": self._get_next_run_time()
        }

    def _get_next_run_time(self) -> str:
        """获取下次执行时间"""
        now = datetime.utcnow()
        next_run = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if now.hour >= 0:
            next_run = next_run + timedelta(days=1)
        return next_run.isoformat()

# 全局调度器实例
scheduler = SystemScheduler()

# 预定义的定时任务
async def daily_system_reset():
    """每日系统重置任务（0点执行）"""
    logger.info("开始执行每日系统重置")

    db = SessionLocal()
    try:
        result = SystemInitService.reset_system(db)
        logger.info(f"每日系统重置完成: {result['summary']}")
        return {
            "success": True,
            "message": "每日系统重置完成",
            "summary": result["summary"],
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"每日系统重置失败: {str(e)}")
        return {
            "success": False,
            "message": f"每日系统重置失败: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }
    finally:
        db.close()

async def cleanup_old_logs():
    """清理旧的审计日志（保留30天）"""
    logger.info("开始清理旧的审计日志")

    db = SessionLocal()
    try:
        from ..models.operation_log import OperationLog
        from datetime import timedelta

        # 删除30天前的日志
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        deleted_count = db.query(OperationLog).filter(
            OperationLog.created_at < cutoff_date
        ).delete()

        db.commit()
        logger.info(f"清理旧审计日志完成，删除 {deleted_count} 条记录")
        return {
            "success": True,
            "message": f"清理旧审计日志完成，删除 {deleted_count} 条记录",
            "deleted_count": deleted_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"清理旧审计日志失败: {str(e)}")
        return {
            "success": False,
            "message": f"清理旧审计日志失败: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }
    finally:
        db.close()

# 注册默认任务
def setup_default_tasks():
    """设置默认的定时任务"""
    # 已清除所有定时任务
    pass