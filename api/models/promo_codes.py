from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, DATE
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class PromoCode(Base):
    __tablename__ = "promo_codes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True)
    discount_percent = Column(DECIMAL(5, 2), nullable=False)
    expiration_date = Column(DATE, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    orders = relationship("Order", back_populates="promo_code")
