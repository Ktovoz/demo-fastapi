from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..core.database import get_db
from ..utils.logger import get_logger
from ..services.role_management_service import RoleManagementService
from ..utils.exceptions import service_exception_handler
from ..schemas.base import BaseResponse
from ..schemas.role import RoleUpdate

router = APIRouter()
logger = get_logger(__name__)

@router.get("/", response_model=BaseResponse)
@router.get("", response_model=BaseResponse)  # 支持不带斜杠
async def get_roles(db: Session = Depends(get_db)):
    """获取角色列表"""
    logger.info("获取角色列表")
    
    try:
        result = RoleManagementService.get_roles_list(db)
        logger.info(f"获取角色列表成功: 共 {len(result)} 个角色")
        return BaseResponse(
            success=True,
            message="获取角色列表成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"获取角色列表失败: {str(e)}")
        raise service_exception_handler(e)

@router.get("/{role_id}", response_model=BaseResponse)
@router.get("/{role_id}/", response_model=BaseResponse)  # 支持带斜杠
async def get_role_detail(
    role_id: str,
    db: Session = Depends(get_db)
):
    """获取角色详情"""
    logger.info(f"获取角色详情: {role_id}")
    
    try:
        role_data = RoleManagementService.get_role_detail(db, role_id)
        logger.info(f"获取角色详情成功: {role_data.get('displayName', role_id)}")
        return BaseResponse(
            success=True,
            message="获取角色详情成功",
            data=role_data
        )
        
    except Exception as e:
        logger.error(f"获取角色详情失败: {str(e)}")
        raise service_exception_handler(e)

@router.put("/{role_id}", response_model=BaseResponse)
async def update_role(
    role_id: str,
    role_data: RoleUpdate,
    db: Session = Depends(get_db)
):
    """更新角色信息"""
    logger.info(f"更新角色信息: {role_id}")
    
    try:
        role_dict = role_data.dict(exclude_unset=True)
        role_data_result = RoleManagementService.update_role(db, role_id, role_dict)
        logger.info(f"角色信息更新成功: {role_data_result.get('displayName')}")
        return BaseResponse(
            success=True,
            message="角色信息更新成功",
            data=role_data_result
        )
        
    except Exception as e:
        logger.error(f"更新角色信息失败: {str(e)}")
        raise service_exception_handler(e)