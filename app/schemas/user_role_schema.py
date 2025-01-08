from pydantic import BaseModel, EmailStr
from typing import Any, Optional

class UserCreate(BaseModel):
    name: Optional[str]
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: Optional[str]
    token_type: Optional[str]
    full_name:  Optional[str]

class TokenData(BaseModel):
    email: Optional[str]

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionCreate(BaseModel):
    name: str
    description: Optional[str] = None