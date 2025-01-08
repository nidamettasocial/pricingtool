from app.utils.constants import *
from app.utils.shared_functions import get_db
from crud.auth_crud import authenticate_user, create_access_token, get_password_hash, get_user_by_email
from models.permissions_model import Permission
from sqlalchemy.orm import Session
from models.role_model import Role
from models.role_permissions import RolePermission
from models.user_model import User
from schemas.user_role_schema import PermissionCreate, RoleCreate, UserCreate, Token
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, status
import jwt as pyjwt 
import datetime


auth_router = APIRouter()



@auth_router.post("/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):

    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = get_password_hash(user.password)  
    new_user = User(email=user.email, hashed_password=hashed_password, full_name = user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate a verification token
    token_data = {"sub": new_user.email}
    create_access_token(token_data, expires_delta=datetime.timedelta(minutes=15))

    return {"message": "Registration Successful"}


@auth_router.post("/roles", response_model=RoleCreate)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    new_role = Role(name=role.name, description=role.description)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@auth_router.post("/permissions", response_model=PermissionCreate)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    new_permission = Permission(name=permission.name, description=permission.description)
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission

@auth_router.post("/assign-permission")
def assign_permission(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
    db.add(role_permission)
    db.commit()

@auth_router.post("/login", response_model=Token)
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email, "full_name" : user.full_name},
        expires_delta=datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(
        access_token= access_token,
        token_type = "Bearer",
        full_name=user.full_name
    )