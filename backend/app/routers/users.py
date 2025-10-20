from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional

from ..core.database import get_db
from ..utils.logger import get_logger
from ..services.user_management_service import UserManagementService
from ..utils.exceptions import service_exception_handler
from ..schemas.base import BaseResponse, PaginatedResponse
from ..schemas.user import UserCreate, UserUpdate, UserListResponse, UserDetailResponse

router = APIRouter()
logger = get_logger(__name__)

@router.get("/", response_model=PaginatedResponse)
@router.get("", response_model=PaginatedResponse)  # 同时支持不带斜杠
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    status: Optional[str] = Query("all", description="状态筛选"),
    role: Optional[str] = Query("all", description="角色筛选"),
    tags: Optional[str] = Query(None, description="标签筛选"),
    department: Optional[str] = Query(None, description="部门筛选"),
    sorter: Optional[str] = Query(None, description="排序"),
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    logger.info(f"获取用户列表: page={page}, pageSize={pageSize}, keyword={keyword}")
    
    try:
        result = UserManagementService.get_users_list(
            db=db,
            page=page,
            page_size=pageSize,
            keyword=keyword,
            status=status,
            role=role,
            sorter=sorter
        )
        
        logger.info(f"获取用户列表成功: 共 {result['total']} 条记录")
        return PaginatedResponse(
            success=True,
            message="获取用户列表成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"获取用户列表失败: {str(e)}")
        raise service_exception_handler(e)

@router.get("/{user_id}", response_model=BaseResponse)
@router.get("/{user_id}/", response_model=BaseResponse)  # 支持带斜杠
async def get_user_detail(
    user_id: str,
    db: Session = Depends(get_db)
):
    """获取用户详情"""
    logger.info(f"获取用户详情: {user_id}")
    
    try:
        user_data = UserManagementService.get_user_detail(db, user_id)
        logger.info(f"获取用户详情成功: {user_data.get('name', user_id)}")
        return BaseResponse(
            success=True,
            message="获取用户详情成功",
            data=user_data
        )
        
    except Exception as e:
        logger.error(f"获取用户详情失败: {str(e)}")
        raise service_exception_handler(e)

@router.post("/", response_model=BaseResponse)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """创建用户"""
    logger.info(f"创建用户: {user_data.email}")
    
    try:
        user_dict = user_data.dict()
        user_dict["name"] = user_dict.pop("name")
        user_dict["email"] = user_dict.pop("email")
        user_dict["password"] = user_dict.pop("password")
        user_dict["avatar"] = user_dict.pop("avatar", None)
        user_dict["role"] = user_dict.pop("role", None)
        
        user_data_result = UserManagementService.create_user(db, user_dict)
        logger.info(f"用户创建成功: {user_data_result.get('email')}")
        return BaseResponse(
            success=True,
            message="用户创建成功",
            data=user_data_result
        )
        
    except Exception as e:
        logger.error(f"创建用户失败: {str(e)}")
        raise service_exception_handler(e)

@router.put("/{user_id}", response_model=BaseResponse)
@router.put("/{user_id}/", response_model=BaseResponse)  # 支持带斜杠
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    logger.info(f"更新用户信息: {user_id}")
    
    try:
        user_dict = user_data.dict(exclude_unset=True)
        user_data_result = UserManagementService.update_user(db, user_id, user_dict)
        logger.info(f"用户信息更新成功: {user_data_result.get('email')}")
        return BaseResponse(
            success=True,
            message="用户信息更新成功",
            data=user_data_result
        )
        
    except Exception as e:
        logger.error(f"更新用户信息失败: {str(e)}")
        raise service_exception_handler(e)

@router.patch("/{user_id}/status", response_model=BaseResponse)
@router.patch("/{user_id}/status/", response_model=BaseResponse)  # 支持带斜杠
async def update_user_status(
    user_id: str,
    status_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """更新用户状态"""
    logger.info(f"更新用户状态: {user_id}")
    
    try:
        result = UserManagementService.update_user_status(db, user_id, status_data)
        logger.info(f"用户状态更新成功: {result.get('id')}")
        return BaseResponse(
            success=True,
            message="用户状态更新成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"更新用户状态失败: {str(e)}")
        raise service_exception_handler(e)

@router.delete("/{user_id}", response_model=BaseResponse)
@router.delete("/{user_id}/", response_model=BaseResponse)  # 支持带斜杠
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """删除用户"""
    logger.info(f"删除用户: {user_id}")
    
    try:
        result = UserManagementService.delete_user(db, user_id)
        logger.info(f"用户删除成功: {user_id}")
        return BaseResponse(
            success=True,
            message="用户删除成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"删除用户失败: {str(e)}")
        raise service_exception_handler(e)

@router.post("/bulk-delete", response_model=BaseResponse)
@router.post("/bulk-delete/", response_model=BaseResponse)  # 支持带斜杠
async def bulk_delete_users(
    delete_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """批量删除用户"""
    logger.info(f"批量删除用户: {delete_data.get('ids')}")
    
    try:
        ids = delete_data.get("ids", [])
        result = UserManagementService.bulk_delete_users(db, ids)
        logger.info(f"批量删除用户成功: 共删除 {result.get('deleted', 0)} 个用户")
        return BaseResponse(
            success=True,
            message="批量删除用户成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"批量删除用户失败: {str(e)}")
        raise service_exception_handler(e)