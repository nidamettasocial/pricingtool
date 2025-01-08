from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.config import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, ForeignKey("roles.name"), default="admin")
    verified = Column(Boolean, default=True)