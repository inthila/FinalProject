from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    quantity = Column(DECIMAL(10, 2), nullable=False, server_default='0.0')
    unit = Column(String(20), nullable=False)
    low_stock_threshold = Column(DECIMAL(10, 2), nullable=False, server_default='10.0')

    menu_items = relationship("MenuItemIngredient", back_populates="ingredient")
    low_stock_alerts = relationship("LowStocksAlert", back_populates="ingredient", cascade="all, delete-orphan")
