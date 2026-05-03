from typing import Optional, List, Literal
from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from .promo_codes import PromoCode
from .order_items import OrderItem, OrderItemCreate


# Shared order fields reused by multiple order schemas
class OrderBase(BaseModel):
    customer_name: str
    customer_phone: str
    customer_address: Optional[str] = None
    order_type: Literal["takeout", "delivery"]
    payment_method: str


# Schema used when creating a new order
class OrderCreate(OrderBase):
    total_price: float
    promo_code_id: Optional[int] = None
    order_items: List[OrderItemCreate] = []


# Schema used for partial order updates, so all fields are optional
class OrderUpdate(BaseModel):
    status: Optional[str] = None
    customer_address: Optional[str] = None
    payment_method: Optional[str] = None


# Schema returned in responses, including the database-generated ID and related data
class Order(OrderBase):
    id: int
    tracking_number: str
    status: str
    total_price: float
    created_at: datetime
    promo_code: Optional[PromoCode] = None
    order_items: List[OrderItem] = []

    model_config = ConfigDict(from_attributes=True)


class OrderRevenue(BaseModel):
    date: date
    revenue: float