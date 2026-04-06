from sqlalchemy import Column, Integer, String, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    calories = Column(Integer, nullable=True)
    category = Column(String(50), nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)

    ingredients = relationship("MenuItemIngredient", back_populates="menu_item", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="menu_item")
