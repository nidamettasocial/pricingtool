from http.client import HTTPException
from app.config import SessionLocal
from app.utils.constants import *
from fastapi import HTTPException, status
from functools import wraps
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def requires_permission(permission: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            if not current_user or permission not in current_user.get("permissions", []):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission '{permission}' is required to perform this action."
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator
