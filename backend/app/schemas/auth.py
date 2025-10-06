from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class LoginRequest(BaseModel):
    """登录请求模型"""
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., min_length=6, max_length=100, description="用户密码")
    remember: Optional[bool] = Field(False, description="记住我")

class RegisterRequest(BaseModel):
    """注册请求模型"""
    name: str = Field(..., min_length=1, max_length=100, description="用户姓名")
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., min_length=6, max_length=100, description="用户密码")

class ForgotPasswordRequest(BaseModel):
    """忘记密码请求模型"""
    email: EmailStr = Field(..., description="用户邮箱")

class UserTokenData(BaseModel):
    """用户令牌数据模型"""
    id: str = Field(..., description="用户ID")
    name: str = Field(..., description="用户姓名")
    email: EmailStr = Field(..., description="用户邮箱")
    role: str = Field(..., description="用户角色")
    permissions: List[str] = Field(..., description="权限列表")
    avatar: Optional[str] = Field(None, description="头像URL")
    lastLogin: Optional[datetime] = Field(None, description="最后登录时间")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z" if v else None
        }

class LoginResponseData(BaseModel):
    """登录响应数据模型"""
    token: str = Field(..., description="访问令牌")
    expiresIn: int = Field(..., description="过期时间(分钟)")
    user: UserTokenData = Field(..., description="用户信息")

class AuthResponse(BaseModel):
    """认证响应模型"""
    success: bool = True
    message: str = ""
    data: Optional[LoginResponseData] = None
    error_code: Optional[str] = None
    timestamp: datetime = datetime.utcnow()

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }