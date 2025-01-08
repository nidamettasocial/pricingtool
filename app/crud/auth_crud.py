from fastapi import Depends, HTTPException
from typing import List
import datetime
from sqlalchemy.orm import Session
from app.config import *
from app.utils.constants import *
from models.user_model import User
from models.role_model import Role
from models.permissions_model import Permission
from models.role_permissions import RolePermission
import jwt as pyjwt 
import quopri

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_context.hash(password)

def create_access_token(data: dict, expires_delta: datetime.timedelta):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = pyjwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_email(db, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_current_user(db: Session = Depends(get_db), token: str = Depends()):
    try:
        payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail=INVALID_TOKEN)
        user = get_user_by_email(db, email)
        if user is None:
            raise HTTPException(status_code=401, detail=USER_NOT_FOUND)
        return user
    except pyjwt.PyJWTError:
        raise HTTPException(status_code=401, detail=INVALID_TOKEN)