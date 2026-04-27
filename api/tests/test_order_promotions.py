from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from ..controllers import orders as controller
from ..models import model_loader  # noqa: F401


def make_request(**overrides):
    data = {
        "customer_name": "John Doe",
        "customer_phone": "555-1234",
        "customer_address": "123 Main St",
        "order_type": "takeout",
        "payment_method": "card",
        "total_price": 20.00,
        "promo_code_id": None,
    }
    data.update(overrides)
    return SimpleNamespace(**data)


def test_create_order_applies_active_promo_discount():
    db = Mock()
    promo_code = SimpleNamespace(id=1, is_active=True, discount_percent=Decimal("25.00"))
    db.query.return_value.filter.return_value.first.return_value = promo_code

    created_order = controller.create(db, make_request(promo_code_id=1))

    assert created_order.total_price == Decimal("15.00")
    assert created_order.promo_code_id == 1


def test_create_order_rejects_missing_promo_code():
    db = Mock()
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        controller.create(db, make_request(promo_code_id=99))

    assert exc.value.status_code == 404
    assert exc.value.detail == "Promo code not found!"


def test_create_order_rejects_inactive_promo_code():
    db = Mock()
    promo_code = SimpleNamespace(id=2, is_active=False, discount_percent=Decimal("10.00"))
    db.query.return_value.filter.return_value.first.return_value = promo_code

    with pytest.raises(HTTPException) as exc:
        controller.create(db, make_request(promo_code_id=2))

    assert exc.value.status_code == 400
    assert exc.value.detail == "Promo code is inactive!"
