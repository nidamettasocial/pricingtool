from app.crud.auth_crud import check_permissions, get_current_user
from app.schemas.products_schema import ProductBase, ProductCreate, ProductUpdate

from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, SessionLocal
from crud.auth_crud import authenticate_user, create_access_token, get_password_hash, get_user_by_email, send_verification_email
from models.permissions_model import Permission
from sqlalchemy.orm import Session
from models.role_model import Role
from models.role_permissions import RolePermission
from models.user_model import User
from models.product_model import Products
from schemas.user_role_schema import PermissionCreate, RoleCreate, UserCreate, Token
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException, status
# from jose import JWTError, jwt
import jwt as pyjwt 
import datetime
from app.config import SessionLocal
from typing import Any, List, Optional 


product_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@product_router.get("/products/", response_model=List[ProductBase])
def get_products(name: Optional[str] = None, category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Products)
    
    if name:
        query = query.filter(Products.name.ilike(f"%{name}%"))
    
    if category:
        query = query.filter(Products.category.ilike(f"%{category}%"))
    
    products = query.all()
    return products


@product_router.get("/products/{product_id}", response_model=ProductBase)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Products).filter(Products.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@product_router.post("/products/", response_model=ProductBase)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    demand_forecast = 121531
    db_product = Products(name=product.name, category=product.category, cost_price=product.cost_price,
                         selling_price=product.selling_price, description=product.description,
                         stock_available=product.stock_available, units_sold = product.units_sold, demand_forecast = demand_forecast)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@product_router.put("/products/{product_id}", response_model=ProductBase)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Products).filter(Products.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


@product_router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Products).filter(Products.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}


@product_router.get("/search_products/", response_model=List[ProductBase])
def search_products(name: Optional[str] = None, category: Optional[str] = None, 
                    sort_by: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Products)

    if name:
        query = query.filter(Products.name.ilike(f"%{name}%"))
    
    if category:
        query = query.filter(Products.category.ilike(f"%{category}%"))
    
    # Apply Sorting
    if sort_by:
        if sort_by == "name":
            query = query.order_by(Products.name)
        elif sort_by == "category":
            query = query.order_by(Products.category)
        elif sort_by == "cost_price":
            query = query.order_by(Products.cost_price)
        elif sort_by == "selling_price":
            query = query.order_by(Products.selling_price)
    
    products = query.all()
    return products