from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, SessionLocal
from crud.auth_crud import authenticate_user, create_access_token, get_password_hash, get_user_by_email, send_verification_email
from models.permissions_model import Permission
from sqlalchemy.orm import Session
from models.role_model import Role
from models.role_permissions import RolePermission
from models.user_model import User
from schemas.user_role_schema import PermissionCreate, RoleCreate, UserCreate, Token
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, status
# from jose import JWTError, jwt
import jwt as pyjwt 
import datetime
from app.config import SessionLocal
from typing import Any 


auth_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    verification_token = create_access_token(token_data, expires_delta=datetime.timedelta(minutes=15))
    print("verification_token", verification_token)
    # Send verification email
    await send_verification_email(new_user.email, verification_token)

    return {"message": "Please check your email to verify your account"}

@auth_router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.verified = True
        db.commit()
        return {"message": "Email verified successfully"}
    except pyjwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

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
    return {"message": "Permission assigned to role successfully"}

@auth_router.post("/login", response_model=Token)
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # todo
    # if not user.verified:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Email not verified. Please verify your email to proceed.",
    #     )
    access_token = create_access_token(
        data={"sub": user.email, "full_name" : user.full_name},
        expires_delta=datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}