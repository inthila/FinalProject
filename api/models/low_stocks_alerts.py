from datetime import datetime

from sqlalchemy import Boolean, Column, DATETIME, DECIMAL, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class LowStocksAlert(Base):
    __tablename__ = "low_stocks_alerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity_at_alert = Column(DECIMAL(10, 2), nullable=False, server_default="0.0")
    threshold_at_alert = Column(DECIMAL(10, 2), nullable=False, server_default="10.0")
    is_active = Column(Boolean, nullable=False, server_default="1")
    created_at = Column(DATETIME, default=datetime.now)

    ingredient = relationship("Ingredient", back_populates="low_stock_alerts")
