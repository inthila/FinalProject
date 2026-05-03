from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from ..controllers import orders as controller
from ..dependencies.database import get_db
from ..routers.orders import router


def test_read_by_tracking_number_returns_order():
    db = Mock()
    order = SimpleNamespace(id=1, tracking_number="TRACK123")
    db.query.return_value.filter.return_value.first.return_value = order

    result = controller.read_by_tracking_number(db, "TRACK123")

    assert result is order
    assert result.tracking_number == "TRACK123"


def test_read_by_tracking_number_rejects_missing_order():
    db = Mock()
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        controller.read_by_tracking_number(db, "MISSING1")

    assert exc.value.status_code == 404
    assert exc.value.detail == "Tracking number not found!"


def test_get_order_by_tracking_number_endpoint_returns_order():
    app = FastAPI()
    app.include_router(router)

    order = {
        "id": 1,
        "tracking_number": "TRACK123",
        "customer_name": "John Doe",
        "customer_phone": "555-1234",
        "customer_address": "123 Main St",
        "order_type": "delivery",
        "status": "pending",
        "payment_method": "card",
        "total_price": 19.99,
        "created_at": "2026-05-03T10:00:00",
        "promo_code": {
            "id": 1,
            "code": "SAVE10",
            "discount_percent": 10.0,
            "expiration_date": "2026-12-31",
            "is_active": True,
        },
        "order_items": [],
    }

    def override_get_db():
        yield Mock()

    app.dependency_overrides[get_db] = override_get_db
    app.router.dependency_overrides_provider = app

    client = TestClient(app)

    original = controller.read_by_tracking_number
    controller.read_by_tracking_number = lambda db, tracking_number: order
    try:
        response = client.get("/orders/track/TRACK123")
    finally:
        controller.read_by_tracking_number = original

    assert response.status_code == 200
    assert response.json()["tracking_number"] == "TRACK123"


def test_get_order_by_tracking_number_endpoint_returns_404():
    app = FastAPI()
    app.include_router(router)

    def override_get_db():
        yield Mock()

    app.dependency_overrides[get_db] = override_get_db
    app.router.dependency_overrides_provider = app

    client = TestClient(app)

    def raise_not_found(db, tracking_number):
        raise HTTPException(status_code=404, detail="Tracking number not found!")

    original = controller.read_by_tracking_number
    controller.read_by_tracking_number = raise_not_found
    try:
        response = client.get("/orders/track/MISSING1")
    finally:
        controller.read_by_tracking_number = original

    assert response.status_code == 404
    assert response.json() == {"detail": "Tracking number not found!"}
