import os


INVALID_TOKEN= "Invalid token"
USER_NOT_FOUND = "User not found"
ROLE_NOT_FOUND="Role not found"
PERMISSION_DENIED="Permission denied"
SECRET_KEY =os.getenv("SECRET_KEY")
ALGORITHM =os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES =30