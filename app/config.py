import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

load_dotenv()

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SECRET_KEY =os.getenv("SECRET_KEY")
ALGORITHM =os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES =os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")