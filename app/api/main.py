from fastapi import APIRouter
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, SessionLocal
from crud.auth_crud import authenticate_user, create_access_token, get_password_hash, get_user_by_email, send_verification_email
from models.permissions_model import Permission
from models.role_model import Role
from models.role_permissions import RolePermission
from models.user_model import User
from schemas.user_role_schema import PermissionCreate, RoleCreate, UserCreate, Token
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, status
# from jose import JWTError, jwt
import jwt as pyjwt 
import datetime
from typing import Any 
router = APIRouter()


@router.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to Pricing Tool"}

