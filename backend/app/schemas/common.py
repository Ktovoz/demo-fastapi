from pydantic import BaseModel
from typing import Any, Optional

class ResponseBase(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None
    code: int = 200

class ErrorDetail(BaseModel):
    loc: list[str]
    msg: str
    type: str

class ValidationError(BaseModel):
    detail: list[ErrorDetail]

class HealthCheck(BaseModel):
    status: str
    message: str
    timestamp: str