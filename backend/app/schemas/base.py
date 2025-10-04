from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')

class BaseResponse(BaseModel):
    """基础响应模式"""
    message: str = "操作成功"
    status_code: int = 200

class BasePaginationResponse(BaseModel, Generic[T]):
    """基础分页响应模式"""
    items: List[T]
    total: int
    page: int
    size: int
    has_next: bool = False
    has_prev: bool = False

    @property
    def total_pages(self) -> int:
        if self.size == 0:
            return 0
        return (self.total + self.size - 1) // self.size

    def __init__(self, **data):
        super().__init__(**data)
        self.has_next = self.page < self.total_pages
        self.has_prev = self.page > 1