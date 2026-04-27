from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import orders as model
from ..models import promo_codes as promo_model
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal, ROUND_HALF_UP
import uuid


def create(db: Session, request):
    total_price = Decimal(str(request.total_price))
    promo_code_id = request.promo_code_id

    if promo_code_id is not None:
        promo_code = db.query(promo_model.PromoCode).filter(promo_model.PromoCode.id == promo_code_id).first()
        if not promo_code:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promo code not found!")
        if not promo_code.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promo code is inactive!")

        discount_percent = Decimal(str(promo_code.discount_percent))
        discount_amount = (total_price * discount_percent / Decimal("100")).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )
        total_price = max(Decimal("0.00"), total_price - discount_amount)

    new_item = model.Order(
        tracking_number=str(uuid.uuid4())[:8].upper(),
        customer_name=request.customer_name,
        customer_phone=request.customer_phone,
        customer_address=request.customer_address,
        order_type=request.order_type,
        status="pending",
        payment_method=request.payment_method,
        total_price=total_price,
        promo_code_id=promo_code_id
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
