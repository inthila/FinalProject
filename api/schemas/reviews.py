from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from .order_items import OrderItem


# Shared review fields reused by multiple review schemas
class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None

    # Ensures rating values stay within the allowed 1 to 5 range
    @field_validator("rating")
    @classmethod
    def rating_must_be_valid(cls, x):
        if x < 1 or x > 5:
            raise ValueError("Rating must be between 1 and 5")
        return x


# Schema used when creating a new review
class ReviewCreate(ReviewBase):
    order_item_id: int


# Schema used for partial review updates, so all fields are optional
class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

    # Validates updated ratings only when a new rating value is provided
    @field_validator("rating")
    @classmethod
    def rating_must_be_valid(cls, x):
        if x is not None and (x < 1 or x > 5):
            raise ValueError("Rating must be between 1 and 5")
        return x


# Schema returned in responses, including related order item details and creation timestamp.
class Review(ReviewBase):
    id: int
    order_item: OrderItem = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
