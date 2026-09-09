from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class BaseResponse(BaseModel):
    status: str = "success"
    message: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime = datetime.now()

class LoginResponse(BaseResponse):
    data: Optional[Dict[str, Any]] = None

class AuthResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    user_data: Optional[Dict[str, Any]] = None