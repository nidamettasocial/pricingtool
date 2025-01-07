import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.config import Base
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Text, TIMESTAMP, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = {"extend_existing": True}
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    cost_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(100))
    stock_available = Column(Integer, default=0)
    units_sold = Column(Integer, default=0)
    customer_rating = Column(Numeric(3, 2))
    demand_forecast = Column(Integer)
    optimized_price = Column(Numeric(10, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_name', 'name'),
        Index('idx_category', 'category'),
        Index('idx_stock_available', 'stock_available'),
        Index('idx_units_sold', 'units_sold'),
        Index('idx_customer_rating', 'customer_rating'),
        Index('idx_demand_forecast', 'demand_forecast'),
        Index('idx_optimized_price', 'optimized_price'),
        Index('idx_cost_price', 'cost_price'),
        Index('idx_selling_price', 'selling_price')
    )