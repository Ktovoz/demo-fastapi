from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime

from ..core.database import get_db
from ..models.role import Role
from ..models.user_role import UserRole
from ..models.role_permission import RolePermission
from ..models.permission import Permission
from ..utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/")
async def get_roles(db: Session = Depends(get_db)):
    """获取角色列表"""
    logger.info("获取角色列表")
    
    try:
        # 查询所有角色
        roles = db.query(Role).all()
        
        # 构建返回数据
        result = []
        for role in roles:
            # 获取角色成员数量
            members_count = db.query(UserRole).filter(UserRole.role_id == role.id).count()
            
            # 获取角色权限
            permissions = []
            try:
                for role_permission in role.role_permissions:
                    permissions.append(role_permission.permission.name)
            except Exception as e:
                logger.warning(f"获取角色权限失败: {str(e)}")
            
            # 构建角色数据
            role_data = {
                "id": f"ROLE-{role.id}",
                "displayName": role.name,
                "description": role.description or "",
                "members": members_count,
                "permissions": permissions,
                "status": "active"  # 模拟数据，实际应从角色表获取
            }
            
            result.append(role_data)
        
        logger.info(f"获取角色列表成功: 共 {len(result)} 个角色")
        return result
        
    except Exception as e:
        logger.error(f"获取角色列表失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取角色列表失败"
        )

@router.get("/{role_id}")
async def get_role_detail(
    role_id: str,
    db: Session = Depends(get_db)
):
    """获取角色详情"""
    logger.info(f"获取角色详情: {role_id}")
    
    try:
        # 提取角色ID
        if role_id.startswith("ROLE-"):
            role_id = role_id[5:]
        
        # 查询角色
        role = db.query(Role).filter(Role.id == int(role_id)).first()
        if not role:
            raise HTTPException(
                status_code=404,
                detail="角色不存在"
            )
        
        # 获取角色权限
        permissions = []
        try:
            for role_permission in role.role_permissions:
                permissions.append(role_permission.permission.name)
        except Exception as e:
            logger.warning(f"获取角色权限失败: {str(e)}")
        
        # 构建角色数据
        role_data = {
            "id": f"ROLE-{role.id}",
            "displayName": role.name,
            "description": role.description or "",
            "permissions": permissions,
            "status": "active"  # 模拟数据，实际应从角色表获取
        }
        
        logger.info(f"获取角色详情成功: {role.name}")
        return role_data
        
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="无效的角色ID格式"
        )
    except Exception as e:
        logger.error(f"获取角色详情失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取角色详情失败"
        )

@router.put("/{role_id}")
async def update_role(
    role_id: str,
    role_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """更新角色信息"""
    logger.info(f"更新角色信息: {role_id}")
    
    try:
        # 提取角色ID
        if role_id.startswith("ROLE-"):
            role_id = role_id[5:]
        
        # 查询角色
        role = db.query(Role).filter(Role.id == int(role_id)).first()
        if not role:
            raise HTTPException(
                status_code=404,
                detail="角色不存在"
            )
        
        # 更新基本信息
        if "displayName" in role_data:
            role.name = role_data["displayName"]
        
        if "description" in role_data:
            role.description = role_data["description"]
        
        # 更新最后修改时间
        role.updated_at = datetime.utcnow()
        db.commit()
        
        # 更新权限关联
        if "permissions" in role_data:
            # 删除现有权限关联
            db.query(RolePermission).filter(RolePermission.role_id == role.id).delete()
            
            # 添加新权限关联
            permissions = role_data["permissions"]
            if permissions:
                for permission_name in permissions:
                    permission = db.query(Permission).filter(Permission.name == permission_name).first()
                    if permission:
                        role_permission = RolePermission(role_id=role.id, permission_id=permission.id)
                        db.add(role_permission)
            
            db.commit()
        
        logger.info(f"角色信息更新成功: {role.name}")
        
        # 返回更新后的角色数据
        return await get_role_detail(f"ROLE-{role.id}", db)
        
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="无效的角色ID格式"
        )
    except Exception as e:
        logger.error(f"更新角色信息失败: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="更新角色信息失败"
        )