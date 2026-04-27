import pytest
from pydantic import ValidationError

from ..schemas.orders import OrderCreate


def test_order_create_accepts_takeout():
    order = OrderCreate(
        customer_name="John Doe",
        customer_phone="555-1234",
        customer_address="123 Main St",
        order_type="takeout",
        payment_method="card",
    )

    assert order.order_type == "takeout"


def test_order_create_accepts_delivery():
    order = OrderCreate(
        customer_name="Jane Doe",
        customer_phone="555-5678",
        customer_address="456 Main St",
        order_type="delivery",
        payment_method="cash",
    )

    assert order.order_type == "delivery"


def test_order_create_rejects_invalid_order_type():
    with pytest.raises(ValidationError):
        OrderCreate(
            customer_name="John Doe",
            customer_phone="555-1234",
            customer_address="123 Main St",
            order_type="pickup",
            payment_method="card",
        )
