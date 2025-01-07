from pydantic import BaseModel, EmailStr
from typing import Any, Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: Optional[str]
    token_type: Optional[str]
    strings: Any

class TokenData(BaseModel):
    email: Optional[str]

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionCreate(BaseModel):
    name: str
    description: Optional[str] = None