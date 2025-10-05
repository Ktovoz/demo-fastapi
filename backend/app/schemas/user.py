from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    """用户基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="用户姓名")
    email: EmailStr = Field(..., description="用户邮箱")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")

class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=6, max_length=100, description="用户密码")
    role: Optional[str] = Field(None, description="用户角色")

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('密码长度不能少于6位')
        return v

class UserUpdate(BaseModel):
    """用户更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="用户姓名")
    email: Optional[EmailStr] = Field(None, description="用户邮箱")
    password: Optional[str] = Field(None, min_length=6, max_length=100, description="用户密码")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    role: Optional[str] = Field(None, description="用户角色")

    @validator('password')
    def validate_password(cls, v):
        if v is not None and len(v) < 6:
            raise ValueError('密码长度不能少于6位')
        return v

class UserResponse(UserBase):
    """用户响应模型"""
    id: str = Field(..., description="用户ID")
    role: str = Field(..., description="用户角色")
    roleName: str = Field(..., description="角色名称")
    status: str = Field(..., description="用户状态")
    department: str = Field(..., description="部门")
    phone: str = Field(..., description="电话")
    tags: List[str] = Field(..., description="标签")
    permissions: List[str] = Field(..., description="权限列表")
    createdAt: Optional[datetime] = Field(None, description="创建时间")
    lastLogin: Optional[datetime] = Field(None, description="最后登录时间")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z" if v else None
        }

class UserDetailResponse(UserResponse):
    """用户详情响应模型"""
    pass

class UserListResponse(BaseModel):
    """用户列表响应模型"""
    items: List[UserResponse] = Field(..., description="用户列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    pageSize: int = Field(..., description="每页数量")