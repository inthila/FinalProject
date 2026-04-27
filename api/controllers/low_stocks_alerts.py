from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from ..models import ingredients as model


# returns list of all ingredients whose quantity is less than or equal to their low‑stock threshold
def read_all(db: Session):
    try:
        result = (
            db.query(model.Ingredient)
            .filter(model.Ingredient.quantity <= model.Ingredient.low_stock_threshold)
            .order_by(model.Ingredient.quantity.asc(), model.Ingredient.name.asc())
            .all()
        )
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

# returns one low‑stock ingredient by ID
def read_one(db: Session, item_id: int):
    try:
        item = (
            db.query(model.Ingredient)
            .filter(model.Ingredient.id == item_id)
            .filter(model.Ingredient.quantity <= model.Ingredient.low_stock_threshold)
            .first()
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Low-stock ingredient not found!",
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item
