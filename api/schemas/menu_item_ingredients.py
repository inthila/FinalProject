from typing import Optional
from pydantic import BaseModel, ConfigDict
from .menu_items import MenuItem
from .ingredients import Ingredient


# Shared fields for menu item and ingredient link schemas
class MenuItemIngredientBase(BaseModel):
    quantity_required: float


# Schema used when creating a new menu item ingredient link
class MenuItemIngredientCreate(MenuItemIngredientBase):
    menu_item_id: int
    ingredient_id: int


# Schema used for partial updates to a menu item ingredient link
class MenuItemIngredientUpdate(BaseModel):
    menu_item_id: Optional[int] = None
    ingredient_id: Optional[int] = None
    quantity_required: Optional[float] = None


# Schema returned in responses, including related menu item and ingredient details
class MenuItemIngredient(MenuItemIngredientBase):
    id: int
    menu_item: MenuItem = None
    ingredient: Ingredient = None

    model_config = ConfigDict(from_attributes=True)
