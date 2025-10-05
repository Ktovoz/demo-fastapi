from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class RoleBase(BaseModel):
    """角色基础模型"""
    displayName: str = Field(..., min_length=1, max_length=50, description="角色名称")
    description: Optional[str] = Field(None, max_length=200, description="角色描述")

class RoleCreate(RoleBase):
    """角色创建模型"""
    pass

class RoleUpdate(RoleBase):
    """角色更新模型"""
    pass

class RoleResponse(RoleBase):
    """角色响应模型"""
    id: str = Field(..., description="角色ID")
    members: int = Field(..., description="成员数量")
    permissions: List[str] = Field(..., description="权限列表")
    status: str = Field(..., description="角色状态")

class RoleDetailResponse(RoleResponse):
    """角色详情响应模型"""
    pass

class RoleListResponse(BaseModel):
    """角色列表响应模型"""
    items: List[RoleResponse] = Field(..., description="角色列表")
    total: int = Field(..., description="总数量")