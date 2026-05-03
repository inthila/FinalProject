from datetime import date
from decimal import Decimal
from unittest.mock import Mock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..controllers import orders as controller
from ..dependencies.database import get_db
from ..routers.orders import router


def test_read_revenue_by_date_returns_total():
    db = Mock()
    db.query.return_value.filter.return_value.scalar.return_value = Decimal("42.75")

    result = controller.read_revenue_by_date(db, date(2026, 5, 3))

    assert result == {"date": date(2026, 5, 3), "revenue": 42.75}


def test_read_revenue_by_date_returns_zero_when_no_orders():
    db = Mock()
    db.query.return_value.filter.return_value.scalar.return_value = None

    result = controller.read_revenue_by_date(db, date(2026, 5, 4))

    assert result == {"date": date(2026, 5, 4), "revenue": 0.0}


def test_get_order_revenue_endpoint_returns_summary():
    app = FastAPI()
    app.include_router(router)

    def override_get_db():
        yield Mock()

    app.dependency_overrides[get_db] = override_get_db
    app.router.dependency_overrides_provider = app

    client = TestClient(app)

    original = controller.read_revenue_by_date
    controller.read_revenue_by_date = lambda db, target_date: {
        "date": target_date,
        "revenue": 42.75,
    }
    try:
        response = client.get("/orders/revenue?date=2026-05-03")
    finally:
        controller.read_revenue_by_date = original

    assert response.status_code == 200
    assert response.json() == {"date": "2026-05-03", "revenue": 42.75}
