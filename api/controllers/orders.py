from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import orders as model
from ..models import promo_codes as promo_model
from ..models import menu_items as menu_item_model
from ..models import order_items as order_item_model
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from decimal import Decimal, ROUND_HALF_UP
from datetime import date
import uuid

def create(db: Session, request):
    for item in request.order_items:
        menu_item = db.query(menu_item_model.MenuItem).filter(
            menu_item_model.MenuItem.id == item.menu_item_id
        ).first()
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu item {item.menu_item_id} not found!")
        for link in menu_item.ingredients:
            required = link.quantity_required * item.quantity
            if link.ingredient.quantity < required:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for ingredient: {link.ingredient.name} "
                           f"(need {required} {link.ingredient.unit}, have {link.ingredient.quantity})"
                )

    total_price = Decimal(str(request.total_price))
    promo_code_id = request.promo_code_id

    if promo_code_id is not None:
        promo_code = db.query(promo_model.PromoCode).filter(promo_model.PromoCode.id == promo_code_id).first()
        if not promo_code:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promo code not found!")
        if not promo_code.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promo code is inactive!")
        if promo_code.expiration_date < date.today():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promo code is expired!")

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

        # Save order items
        for item in request.order_items:
            new_order_item = order_item_model.OrderItem(
                order_id=new_item.id,
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                special_instructions=item.special_instructions
            )
            db.add(new_order_item)
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


def read_by_tracking_number(db: Session, tracking_number: str):
    try:
        item = db.query(model.Order).filter(model.Order.tracking_number == tracking_number).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tracking number not found!"
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def read_revenue_by_date(db: Session, target_date: date):
    try:
        revenue = (
            db.query(func.sum(model.Order.total_price))
            .filter(func.date(model.Order.created_at) == target_date)
            .scalar()
        )
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    total_revenue = Decimal(str(revenue or "0.00")).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )
    return {"date": target_date, "revenue": float(total_revenue)}


def read_by_date_range(db: Session, start_date: date, end_date: date):
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be on or before end date!"
        )

    try:
        result = (
            db.query(model.Order)
            .filter(func.date(model.Order.created_at) >= start_date)
            .filter(func.date(model.Order.created_at) <= end_date)
            .order_by(model.Order.created_at.asc())
            .all()
        )
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


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
