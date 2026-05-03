from ..controllers import orders as controller
import pytest
from types import SimpleNamespace
from decimal import Decimal

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_order(db_session):
    order_request = SimpleNamespace(
        customer_name="John Doe",
        customer_phone="555-1234",
        customer_address="123 Main St",
        order_type="delivery",
        payment_method="card",
        total_price=25.00,
        promo_code_id=None,
    )

    created_order = controller.create(db_session, order_request)

    assert created_order is not None
    assert created_order.customer_name == "John Doe"
    assert created_order.customer_phone == "555-1234"
    assert created_order.total_price == Decimal("25.0")
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(created_order)
