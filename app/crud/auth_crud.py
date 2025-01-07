from fastapi import Depends, HTTPException
# from jose import JWTError, jwt
from typing import List
import datetime
from sqlalchemy.orm import Session
# import aiosmtplib
from email.mime.text import MIMEText
from app.config import *
from models.user_model import User
from models.role_model import Role
from models.permissions_model import Permission
from models.role_permissions import RolePermission
import jwt as pyjwt 



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
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user_by_email(db, email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except pyjwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def check_permissions(user: User, required_permissions: List[str], db: SessionLocal):
    role = db.query(Role).filter(Role.name == user.role).first()
    if not role:
        raise HTTPException(status_code=403, detail="Role not found")
    permissions = db.query(Permission).join(RolePermission).filter(RolePermission.role_id == role.id).all()
    user_permissions = {permission.name for permission in permissions}
    if not all(permission in user_permissions for permission in required_permissions):
        raise HTTPException(status_code=403, detail="Permission denied")

async def send_verification_email(email: str, token: str):
    verification_link = f"http://yourdomain.com/verify-email?token={token}"
    message = MIMEText(f"Click here to verify your email: {verification_link}")
    message["Subject"] = "Verify Your Email"
    message["From"] = "noreply@yourdomain.com"
    message["To"] = email

    # await aiosmtplib.send(
    #     message,
    #     hostname="smtp.your-email-provider.com",
    #     port=587,
    #     username="your-email@example.com",
    #     password="your-email-password",
    #     use_tls=True,
    # )