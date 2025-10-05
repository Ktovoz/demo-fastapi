from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..utils.logger import get_logger
from ..services.system_management_service import SystemManagementService
from ..services.system_init_service import SystemInitService
from ..utils.exceptions import service_exception_handler
from ..schemas.base import BaseResponse, PaginatedResponse
from ..schemas.system import SystemSettingsUpdate
from ..core.security import get_current_user
from ..models.user import User

router = APIRouter()
logger = get_logger(__name__)

@router.get("/logs", response_model=PaginatedResponse)
async def get_system_logs(
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    level: Optional[str] = Query("ALL", description="日志级别筛选"),
    sorter: Optional[str] = Query(None, description="排序"),
    db: Session = Depends(get_db)
):
    """获取系统日志"""
    logger.info(f"获取系统日志: page={page}, pageSize={pageSize}, keyword={keyword}, level={level}")
    
    try:
        result = SystemManagementService.get_system_logs(
            db=db,
            page=page,
            page_size=pageSize,
            keyword=keyword,
            level=level,
            sorter=sorter
        )
        
        logger.info(f"获取系统日志成功: 共 {result['total']} 条记录")
        return PaginatedResponse(
            success=True,
            message="获取系统日志成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"获取系统日志失败: {str(e)}")
        raise service_exception_handler(e)

@router.get("/logs/summary", response_model=BaseResponse)
async def get_logs_summary(db: Session = Depends(get_db)):
    """获取日志概览数据"""
    logger.info("获取日志概览数据")
    
    try:
        result = SystemManagementService.get_logs_summary(db)
        logger.info("获取日志概览数据成功")
        return BaseResponse(
            success=True,
            message="获取日志概览数据成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"获取日志概览数据失败: {str(e)}")
        raise service_exception_handler(e)

@router.get("/settings", response_model=BaseResponse)
async def get_system_settings():
    """获取系统设置"""
    logger.info("获取系统设置")
    
    try:
        settings_data = SystemManagementService.get_system_settings()
        logger.info("获取系统设置成功")
        return BaseResponse(
            success=True,
            message="获取系统设置成功",
            data=settings_data
        )
        
    except Exception as e:
        logger.error(f"获取系统设置失败: {str(e)}")
        raise service_exception_handler(e)

@router.put("/settings", response_model=BaseResponse)
async def update_system_settings(
    settings_data: SystemSettingsUpdate
):
    """更新系统设置"""
    logger.info("更新系统设置")
    
    try:
        settings_dict = settings_data.dict(exclude_unset=True)
        settings_data_result = SystemManagementService.update_system_settings(settings_dict)
        logger.info("系统设置更新成功")
        return BaseResponse(
            success=True,
            message="系统设置更新成功",
            data=settings_data_result
        )
        
    except Exception as e:
        logger.error(f"更新系统设置失败: {str(e)}")
        raise service_exception_handler(e)

@router.get("/performance", response_model=BaseResponse)
async def get_performance_stats():
    """获取性能统计信息"""
    logger.info("获取性能统计信息")
    
    try:
        from ..utils.performance import performance_monitor
        stats = performance_monitor.get_summary()
        logger.info("获取性能统计信息成功")
        return BaseResponse(
            success=True,
            message="获取性能统计信息成功",
            data=stats
        )
        
    except Exception as e:
        logger.error(f"获取性能统计信息失败: {str(e)}")
        raise service_exception_handler(e)

@router.get("/performance/requests", response_model=BaseResponse)
async def get_request_stats():
    """获取请求统计信息"""
    logger.info("获取请求统计信息")
    
    try:
        from ..utils.performance import performance_monitor
        stats = performance_monitor.get_request_stats()
        logger.info("获取请求统计信息成功")
        return BaseResponse(
            success=True,
            message="获取请求统计信息成功",
            data=stats
        )
        
    except Exception as e:
        logger.error(f"获取请求统计信息失败: {str(e)}")
        raise service_exception_handler(e)

@router.get("/performance/slow", response_model=BaseResponse)
async def get_slow_requests(threshold: float = 1.0):
    """获取慢请求列表"""
    logger.info(f"获取慢请求列表: threshold={threshold}s")
    
    try:
        from ..utils.performance import performance_monitor
        slow_requests = performance_monitor.get_slow_requests(threshold)
        logger.info(f"获取慢请求列表成功: 共 {len(slow_requests)} 个慢请求")
        return BaseResponse(
            success=True,
            message="获取慢请求列表成功",
            data=slow_requests
        )
        
    except Exception as e:
        logger.error(f"获取慢请求列表失败: {str(e)}")
        raise service_exception_handler(e)

@router.delete("/performance/reset", response_model=BaseResponse)
async def reset_performance_stats():
    """重置性能统计数据"""
    logger.info("重置性能统计数据")
    
    try:
        from ..utils.performance import performance_monitor
        performance_monitor.reset_stats()
        logger.info("性能统计数据重置成功")
        return BaseResponse(
            success=True,
            message="性能统计数据重置成功",
            data={}
        )
        
    except Exception as e:
        logger.error(f"重置性能统计数据失败: {str(e)}")
        raise service_exception_handler(e)

@router.get("/cache/stats", response_model=BaseResponse)
async def get_cache_stats():
    """获取缓存统计信息"""
    logger.info("获取缓存统计信息")
    
    try:
        from ..utils.cache import cache
        stats = cache.stats()
        logger.info("获取缓存统计信息成功")
        return BaseResponse(
            success=True,
            message="获取缓存统计信息成功",
            data=stats
        )
        
    except Exception as e:
        logger.error(f"获取缓存统计信息失败: {str(e)}")
        raise service_exception_handler(e)

@router.delete("/cache/clear", response_model=BaseResponse)
async def clear_cache():
    """清空缓存"""
    logger.info("清空缓存")

    try:
        from ..utils.cache import cache
        count = cache.clear()
        logger.info(f"缓存清空成功，共删除 {count} 项")
        return BaseResponse(
            success=True,
            message="缓存清空成功",
            data={"deleted": count}
        )

    except Exception as e:
        logger.error(f"清空缓存失败: {str(e)}")
        raise service_exception_handler(e)

@router.get("/system/status", response_model=BaseResponse)
async def get_system_status(db: Session = Depends(get_db)):
    """获取系统状态"""
    logger.info("获取系统状态")

    try:
        status = SystemInitService.get_system_status(db)
        logger.info("获取系统状态成功")
        return BaseResponse(
            success=True,
            message="获取系统状态成功",
            data=status
        )

    except Exception as e:
        logger.error(f"获取系统状态失败: {str(e)}")
        raise service_exception_handler(e)

@router.post("/system/fix-admin", response_model=BaseResponse)
async def fix_admin_superuser(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """修复admin用户的superuser权限（临时接口）"""
    logger.info(f"用户 {current_user.username} 请求修复admin权限")

    try:
        # 查找admin用户
        admin_user = db.query(User).filter(
            (User.username == "admin") | (User.email == "admin@example.com")
        ).first()

        if not admin_user:
            return BaseResponse(
                success=False,
                message="未找到admin用户"
            )

        # 更新admin用户的superuser权限
        admin_user.is_superuser = True
        db.commit()
        db.refresh(admin_user)

        logger.info(f"成功修复admin用户权限: {admin_user.username} (is_superuser={admin_user.is_superuser})")

        return BaseResponse(
            success=True,
            message="admin用户权限修复成功",
            data={
                "user_id": admin_user.id,
                "username": admin_user.username,
                "email": admin_user.email,
                "is_superuser": admin_user.is_superuser
            }
        )

    except Exception as e:
        logger.error(f"修复admin用户权限失败: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"修复admin权限失败: {str(e)}"
        )

@router.post("/system/reset", response_model=BaseResponse)
async def reset_system(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """系统初始化（仅超级管理员）"""
    logger.info(f"用户 {current_user.username} 请求系统初始化")

    # 检查权限 - 只有超级管理员可以执行
    if not current_user.is_superuser:
        logger.warning(f"用户 {current_user.username} 尝试执行系统初始化，权限不足")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有超级管理员可以执行系统初始化"
        )

    try:
        # 手动记录初始化开始日志
        from ..models.operation_log import OperationLog
        init_log = OperationLog(
            user_id=current_user.id,
            action="手动系统初始化",
            resource="system",
            description=f"用户 {current_user.username} 手动执行系统初始化",
            ip_address="127.0.0.1",  # 这里可以从request获取真实IP
            user_agent="System Management Interface"
        )
        db.add(init_log)
        db.commit()

        # 执行系统初始化
        result = SystemInitService.reset_system(db)

        logger.info(f"系统初始化成功: {result['summary']}")
        return BaseResponse(
            success=True,
            message="系统初始化成功",
            data=result
        )

    except Exception as e:
        logger.error(f"系统初始化失败: {str(e)}")
        raise service_exception_handler(e)