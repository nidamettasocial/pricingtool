from http.client import HTTPException
from app.crud.auth_crud import get_current_user
from app.schemas.products_schema import ProductBase, ProductCreate, ProductUpdate
from sqlalchemy.orm import Session
from app.utils.shared_functions import get_db, requires_permission
from models.product_model import Products
from fastapi import APIRouter, Depends
from typing import Any, List, Optional 


product_router = APIRouter()

# Endpoint to get a list of products with optional filtering by name or category
@product_router.get("/products/", response_model=List[ProductBase])
def get_products(name: Optional[str] = None, category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Products)
    
    if name:
        query = query.filter(Products.name.ilike(f"%{name}%"))
    
    if category:
        query = query.filter(Products.category.ilike(f"%{category}%"))
    
    products = query.all()
    return products

# Endpoint to get details of a single product by its ID
@product_router.get("/products/{product_id}", response_model=ProductBase)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Products).filter(Products.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Endpoint to create a new product
@product_router.post("/products/", response_model=ProductBase)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    demand_forecast = product.units_sold + (product.units_sold * (product.stock_available / 1000))

    optimized_price = product.cost_price + ((product.selling_price - product.cost_price) / 2) * (demand_forecast / product.units_sold)

    db_product = Products(name=product.name, category=product.category, cost_price=product.cost_price,
                         selling_price=product.selling_price, description=product.description,
                         stock_available=product.stock_available, units_sold = product.units_sold, demand_forecast = demand_forecast, optimized_price = optimized_price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Endpoint to update an existing product
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

# Endpoint to delete a product by its ID
@product_router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Products).filter(Products.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

# Endpoint to search for products with optional sorting
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