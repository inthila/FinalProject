from datetime import date
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from ..controllers import orders as controller
from ..dependencies.database import get_db
from ..routers.orders import router


def test_read_by_date_range_returns_orders():
    db = Mock()
    orders = [SimpleNamespace(id=1), SimpleNamespace(id=2)]
    query = db.query.return_value
    query.filter.return_value.filter.return_value.order_by.return_value.all.return_value = orders

    result = controller.read_by_date_range(db, date(2026, 5, 1), date(2026, 5, 3))

    assert result == orders


def test_read_by_date_range_rejects_invalid_range():
    db = Mock()

    with pytest.raises(HTTPException) as exc:
        controller.read_by_date_range(db, date(2026, 5, 4), date(2026, 5, 3))

    assert exc.value.status_code == 400
    assert exc.value.detail == "Start date must be on or before end date!"


def test_get_orders_by_date_range_endpoint_returns_orders():
    app = FastAPI()
    app.include_router(router)

    def override_get_db():
        yield Mock()

    app.dependency_overrides[get_db] = override_get_db
    app.router.dependency_overrides_provider = app

    client = TestClient(app)

    orders = [
        {
            "id": 1,
            "tracking_number": "TRACK123",
            "customer_name": "John Doe",
            "customer_phone": "555-1234",
            "customer_address": "123 Main St",
            "order_type": "delivery",
            "status": "pending",
            "payment_method": "card",
            "total_price": 19.99,
            "created_at": "2026-05-01T10:00:00",
            "promo_code": {
                "id": 1,
                "code": "SAVE10",
                "discount_percent": 10.0,
                "expiration_date": "2026-12-31",
                "is_active": True,
            },
            "order_items": [],
        },
        {
            "id": 2,
            "tracking_number": "TRACK456",
            "customer_name": "Jane Doe",
            "customer_phone": "555-5678",
            "customer_address": "456 Main St",
            "order_type": "takeout",
            "status": "completed",
            "payment_method": "cash",
            "total_price": 14.5,
            "created_at": "2026-05-03T12:30:00",
            "promo_code": {
                "id": 2,
                "code": "SAVE15",
                "discount_percent": 15.0,
                "expiration_date": "2026-12-31",
                "is_active": True,
            },
            "order_items": [],
        },
    ]

    original = controller.read_by_date_range
    controller.read_by_date_range = lambda db, start_date, end_date: orders
    try:
        response = client.get("/orders/daterange?start=2026-05-01&end=2026-05-03")
    finally:
        controller.read_by_date_range = original

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert [order["tracking_number"] for order in response.json()] == ["TRACK123", "TRACK456"]


def test_get_orders_by_date_range_endpoint_returns_400_for_invalid_range():
    app = FastAPI()
    app.include_router(router)

    def override_get_db():
        yield Mock()

    app.dependency_overrides[get_db] = override_get_db
    app.router.dependency_overrides_provider = app

    client = TestClient(app)

    def raise_invalid_range(db, start_date, end_date):
        raise HTTPException(status_code=400, detail="Start date must be on or before end date!")

    original = controller.read_by_date_range
    controller.read_by_date_range = raise_invalid_range
    try:
        response = client.get("/orders/daterange?start=2026-05-04&end=2026-05-03")
    finally:
        controller.read_by_date_range = original

    assert response.status_code == 400
    assert response.json() == {"detail": "Start date must be on or before end date!"}
