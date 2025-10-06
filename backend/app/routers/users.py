from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from ..core.database import get_db
from ..models.user import User
from ..models.user_role import UserRole
from ..models.role import Role
from ..utils.security import get_password_hash
from ..utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/")
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
        # 构建查询
        query = db.query(User)
        
        # 关键词搜索
        if keyword:
            query = query.filter(
                or_(
                    User.full_name.like(f"%{keyword}%"),
                    User.email.like(f"%{keyword}%"),
                    User.username.like(f"%{keyword}%")
                )
            )
        
        # 状态筛选
        if status != "all":
            # 这里假设User模型有status字段，如果没有，可以基于其他逻辑
            pass
        
        # 角色筛选
        if role != "all":
            query = query.join(UserRole).join(Role).filter(Role.name == role)
        
        # 排序处理
        if sorter:
            try:
                sorter_data = json.loads(sorter) if isinstance(sorter, str) else sorter
                field = sorter_data.get("field", "id")
                order = sorter_data.get("order", "ascend")
                
                # 映射字段名
                field_mapping = {
                    "name": User.full_name,
                    "email": User.email,
                    "lastLogin": User.last_login,
                    "createdAt": User.created_at
                }
                
                if field in field_mapping:
                    if order == "descend":
                        query = query.order_by(field_mapping[field].desc())
                    else:
                        query = query.order_by(field_mapping[field].asc())
            except Exception as e:
                logger.warning(f"排序参数解析失败: {str(e)}")
                # 使用默认排序
                query = query.order_by(User.id)
        else:
            # 默认排序
            query = query.order_by(User.id)
        
        # 计算总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * pageSize
        users = query.offset(offset).limit(pageSize).all()
        
        # 构建返回数据
        items = []
        for user in users:
            # 获取用户角色
            user_roles = []
            try:
                for user_role in user.user_roles:
                    user_roles.append(user_role.role.name)
            except Exception as e:
                logger.warning(f"获取用户角色失败: {str(e)}")
            
            # 获取用户权限
            user_permissions = []
            try:
                for user_role in user.user_roles:
                    for role_permission in user_role.role.role_permissions:
                        user_permissions.append(role_permission.permission.name)
                user_permissions = list(set(user_permissions))
            except Exception as e:
                logger.warning(f"获取用户权限失败: {str(e)}")
            
            # 构建用户数据
            user_data = {
                "id": f"USR-{user.id}",
                "name": user.full_name or user.username,
                "email": user.email,
                "role": user_roles[0] if user_roles else "user",
                "roleName": user_roles[0] if user_roles else "普通用户",
                "department": "技术部",  # 模拟数据，实际应从用户表获取
                "status": "active",  # 模拟数据，实际应从用户表获取
                "lastLogin": user.last_login.isoformat() + "Z" if user.last_login else None,
                "avatar": user.avatar,
                "tags": ["北京"],  # 模拟数据，实际应从用户表获取
                "permissions": user_permissions[:5]  # 只显示前5个权限
            }
            
            items.append(user_data)
        
        result = {
            "items": items,
            "total": total,
            "page": page,
            "pageSize": pageSize
        }
        
        logger.info(f"获取用户列表成功: 共 {total} 条记录")
        return result
        
    except Exception as e:
        logger.error(f"获取用户列表失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取用户列表失败"
        )

@router.get("/{user_id}")
async def get_user_detail(
    user_id: str,
    db: Session = Depends(get_db)
):
    """获取用户详情"""
    logger.info(f"获取用户详情: {user_id}")
    
    try:
        # 提取用户ID
        if user_id.startswith("USR-"):
            user_id = user_id[4:]
        
        # 查询用户
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )
        
        # 获取用户角色
        user_roles = []
        try:
            for user_role in user.user_roles:
                user_roles.append(user_role.role.name)
        except Exception as e:
            logger.warning(f"获取用户角色失败: {str(e)}")
        
        # 获取用户权限
        user_permissions = []
        try:
            for user_role in user.user_roles:
                for role_permission in user_role.role.role_permissions:
                    user_permissions.append(role_permission.permission.name)
            user_permissions = list(set(user_permissions))
        except Exception as e:
            logger.warning(f"获取用户权限失败: {str(e)}")
        
        # 构建用户数据
        user_data = {
            "id": f"USR-{user.id}",
            "name": user.full_name or user.username,
            "email": user.email,
            "role": user_roles[0] if user_roles else "user",
            "roleName": user_roles[0] if user_roles else "普通用户",
            "status": "active",  # 模拟数据，实际应从用户表获取
            "department": "技术部",  # 模拟数据，实际应从用户表获取
            "phone": "+86-13800138000",  # 模拟数据，实际应从用户表获取
            "tags": ["北京", "前端"],  # 模拟数据，实际应从用户表获取
            "permissions": user_permissions,
            "avatar": user.avatar,
            "createdAt": user.created_at.isoformat() + "Z" if user.created_at else None,
            "lastLogin": user.last_login.isoformat() + "Z" if user.last_login else None
        }
        
        logger.info(f"获取用户详情成功: {user.username}")
        return user_data
        
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="无效的用户ID格式"
        )
    except Exception as e:
        logger.error(f"获取用户详情失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取用户详情失败"
        )

@router.post("/")
async def create_user(
    user_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """创建用户"""
    logger.info(f"创建用户: {user_data.get('email')}")
    
    try:
        # 验证必填字段
        required_fields = ["name", "email", "password"]
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                raise HTTPException(
                    status_code=400,
                    detail=f"字段 {field} 不能为空"
                )
        
        # 检查邮箱是否已存在
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="邮箱已被注册"
            )
        
        # 生成用户名
        username = user_data["email"].split("@")[0]
        existing_username = db.query(User).filter(User.username == username).first()
        if existing_username:
            import random
            username = f"{username}{random.randint(1000, 9999)}"
        
        # 创建用户
        hashed_password = get_password_hash(user_data["password"])
        new_user = User(
            username=username,
            email=user_data["email"],
            password_hash=hashed_password,
            full_name=user_data["name"],
            avatar=user_data.get("avatar")
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # 如果指定了角色，添加角色关联
        if "role" in user_data and user_data["role"]:
            role = db.query(Role).filter(Role.name == user_data["role"]).first()
            if role:
                user_role = UserRole(user_id=new_user.id, role_id=role.id)
                db.add(user_role)
                db.commit()
        
        logger.info(f"用户创建成功: {new_user.email}")
        
        # 返回创建的用户数据
        return await get_user_detail(f"USR-{new_user.id}", db)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建用户失败: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="创建用户失败"
        )

@router.put("/{user_id}")
async def update_user(
    user_id: str,
    user_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    logger.info(f"更新用户信息: {user_id}")
    
    try:
        # 提取用户ID
        if user_id.startswith("USR-"):
            user_id = user_id[4:]
        
        # 查询用户
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )
        
        # 更新基本信息
        if "name" in user_data:
            user.full_name = user_data["name"]
        
        if "email" in user_data and user_data["email"] != user.email:
            # 检查邮箱是否已被其他用户使用
            existing_user = db.query(User).filter(
                and_(User.email == user_data["email"], User.id != user.id)
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="邮箱已被其他用户使用"
                )
            user.email = user_data["email"]
        
        if "avatar" in user_data:
            user.avatar = user_data["avatar"]
        
        # 如果提供了密码，更新密码
        if "password" in user_data and user_data["password"]:
            user.password_hash = get_password_hash(user_data["password"])
        
        db.commit()
        
        # 更新角色关联
        if "role" in user_data:
            # 删除现有角色关联
            db.query(UserRole).filter(UserRole.user_id == user.id).delete()
            
            # 添加新角色关联
            if user_data["role"]:
                role = db.query(Role).filter(Role.name == user_data["role"]).first()
                if role:
                    user_role = UserRole(user_id=user.id, role_id=role.id)
                    db.add(user_role)
            
            db.commit()
        
        logger.info(f"用户信息更新成功: {user.email}")
        
        # 返回更新后的用户数据
        return await get_user_detail(f"USR-{user.id}", db)
        
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="无效的用户ID格式"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新用户信息失败: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="更新用户信息失败"
        )

@router.patch("/{user_id}/status")
async def update_user_status(
    user_id: str,
    status_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """更新用户状态"""
    logger.info(f"更新用户状态: {user_id}")
    
    try:
        # 提取用户ID
        if user_id.startswith("USR-"):
            user_id = user_id[4:]
        
        # 查询用户
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )
        
        # 这里假设User模型有status字段，如果没有，可以考虑其他方式
        # 例如使用is_active字段或者添加一个status字段到User模型
        
        # 更新最后修改时间
        user.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"用户状态更新成功: {user.email}")
        
        # 返回更新后的用户数据
        return {
            "id": f"USR-{user.id}",
            "status": status_data.get("status", "active")
        }
        
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="无效的用户ID格式"
        )
    except Exception as e:
        logger.error(f"更新用户状态失败: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="更新用户状态失败"
        )

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """删除用户"""
    logger.info(f"删除用户: {user_id}")
    
    try:
        # 提取用户ID
        if user_id.startswith("USR-"):
            user_id = user_id[4:]
        
        # 查询用户
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="用户不存在"
            )
        
        # 删除用户（级联删除相关关联）
        db.delete(user)
        db.commit()
        
        logger.info(f"用户删除成功: {user.email}")
        
        return {"deleted": True}
        
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="无效的用户ID格式"
        )
    except Exception as e:
        logger.error(f"删除用户失败: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="删除用户失败"
        )

@router.post("/bulk-delete")
async def bulk_delete_users(
    delete_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """批量删除用户"""
    logger.info(f"批量删除用户: {delete_data.get('ids')}")
    
    try:
        ids = delete_data.get("ids", [])
        if not ids:
            raise HTTPException(
                status_code=400,
                detail="请提供要删除的用户ID列表"
            )
        
        # 提取用户ID
        user_ids = []
        for user_id in ids:
            if user_id.startswith("USR-"):
                user_ids.append(int(user_id[4:]))
            else:
                user_ids.append(int(user_id))
        
        # 查询并删除用户
        deleted_count = db.query(User).filter(User.id.in_(user_ids)).delete(synchronize_session=False)
        db.commit()
        
        logger.info(f"批量删除用户成功: 共删除 {deleted_count} 个用户")
        
        return {"deleted": deleted_count}
        
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="无效的用户ID格式"
        )
    except Exception as e:
        logger.error(f"批量删除用户失败: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="批量删除用户失败"
        )