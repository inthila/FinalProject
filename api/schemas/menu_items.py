from typing import Optional
from pydantic import BaseModel, ConfigDict


# Shared menu item fields reused by multiple menu item schemas
class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    calories: Optional[int] = None
    category: str
    is_available: bool = True


# Schema used when creating a new menu item
class MenuItemCreate(MenuItemBase):
    pass


# Schema used for partial menu item updates, so all fields are optional
class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None


# Schema returned in responses, including the database-generated ID
class MenuItem(MenuItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
