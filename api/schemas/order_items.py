from typing import Optional
from pydantic import BaseModel, ConfigDict
from .menu_items import MenuItem


# Shared fields reused by multiple order item schemas
class OrderItemBase(BaseModel):
    quantity: int = 1
    special_instructions: Optional[str] = None


# Schema used when creating a new order item
class OrderItemCreate(OrderItemBase):
    order_id: int
    menu_item_id: int


# Schema used for partial order item updates, so all fields are optional
class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None
    special_instructions: Optional[str] = None


# Schema returned in responses, including the related menu item details
class OrderItem(OrderItemBase):
    id: int
    menu_item: MenuItem = None

    model_config = ConfigDict(from_attributes=True)
