from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date


# Shared promo code fields reused by multiple promo code schemas.
class PromoCodeBase(BaseModel):
    code: str
    discount_percent: float
    expiration_date: date
    is_active: bool = True


# Schema used when creating a new promo code.
class PromoCodeCreate(PromoCodeBase):
    pass


# Schema used for partial promo code updates, so all fields are optional.
class PromoCodeUpdate(BaseModel):
    code: Optional[str] = None
    discount_percent: Optional[float] = None
    expiration_date: Optional[date] = None
    is_active: Optional[bool] = None


# Schema returned in responses, including the database-generated ID.
class PromoCode(PromoCodeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
