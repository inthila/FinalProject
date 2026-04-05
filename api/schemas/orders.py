from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from .order_details import OrderDetail


class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: datetime
    order_details: list[OrderDetail] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
