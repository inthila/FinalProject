from typing import Optional
from pydantic import BaseModel, ConfigDict


# Shared ingredient fields reused by multiple ingredient schemas
class IngredientBase(BaseModel):
    name: str
    quantity: float
    unit: str
    low_stock_threshold: float = 10.0


# Schema used when creating a new ingredient
class IngredientCreate(IngredientBase):
    pass


# Schema used for partial ingredient updates, so all fields are optional
class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    low_stock_threshold: Optional[float] = None


# Schema returned in responses, including the database-generated ID
class Ingredient(IngredientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
