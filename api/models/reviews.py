from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_item_id = Column(Integer, ForeignKey("order_items.id"), unique=True)
    rating = Column(Integer, nullable=False, index=True)
    comment = Column(String(1000), nullable=True)
    created_at = Column(DATETIME, default=datetime.now)

    order_item = relationship("OrderItem", back_populates="review")
