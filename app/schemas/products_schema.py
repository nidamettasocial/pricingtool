from pydantic import BaseModel, EmailStr
from typing import Any, Optional

class ProductBase(BaseModel):
    product_id: int
    name: str
    category: str
    cost_price: float
    selling_price: float
    description: str
    stock_available: int
    units_sold: int
    demand_forecast: Optional[int]
    optimized_price: Optional[int]

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str
    category: str
    cost_price: float
    selling_price: float
    description: str
    stock_available: int
    units_sold: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    cost_price: Optional[float] = None
    selling_price: Optional[float] = None
    description: Optional[str] = None
    stock_available: Optional[int] = None
    units_sold: int