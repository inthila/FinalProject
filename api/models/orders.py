from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tracking_number = Column(String(20), nullable=False, unique=True)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    customer_address = Column(String(300), nullable=True)
    order_type = Column(String(10), nullable=False)        # "takeout" or "delivery"
    status = Column(String(20), nullable=False, server_default='pending')
    payment_method = Column(String(30), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False, server_default='0.0')
    promo_code_id = Column(Integer, ForeignKey("promo_codes.id"), nullable=True)
    created_at = Column(DATETIME, default=datetime.now)

    promo_code = relationship("PromoCode", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
