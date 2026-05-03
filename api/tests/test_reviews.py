from unittest.mock import Mock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..controllers import reviews as controller
from ..dependencies.database import get_db
from ..routers.reviews import router


def test_read_low_rated_returns_reviews():
    db = Mock()
    reviews = [Mock(id=1, rating=1), Mock(id=2, rating=2)]
    db.query.return_value.filter.return_value.all.return_value = reviews

    result = controller.read_low_rated(db)

    assert result == reviews
    db.query.return_value.filter.return_value.all.assert_called_once()


def test_get_low_rated_reviews_endpoint_returns_reviews():
    app = FastAPI()
    app.include_router(router)

    def override_get_db():
        yield Mock()

    app.dependency_overrides[get_db] = override_get_db
    app.router.dependency_overrides_provider = app

    client = TestClient(app)

    low_rated_reviews = [
        {
            "id": 1,
            "rating": 1,
            "comment": "Cold sandwich",
            "created_at": "2026-05-03T10:00:00",
            "order_item": {
                "id": 7,
                "quantity": 1,
                "special_instructions": None,
                "menu_item": {
                    "id": 4,
                    "name": "Turkey Club",
                    "description": "Toasted",
                    "price": 9.99,
                    "calories": 650,
                    "category": "sandwich",
                    "is_available": True,
                },
            },
        },
        {
            "id": 2,
            "rating": 2,
            "comment": "Late delivery",
            "created_at": "2026-05-03T11:00:00",
            "order_item": {
                "id": 8,
                "quantity": 2,
                "special_instructions": "No onions",
                "menu_item": {
                    "id": 5,
                    "name": "Veggie Melt",
                    "description": "Grilled",
                    "price": 8.49,
                    "calories": 540,
                    "category": "sandwich",
                    "is_available": True,
                },
            },
        },
    ]

    original = controller.read_low_rated
    controller.read_low_rated = lambda db: low_rated_reviews
    try:
        response = client.get("/reviews/lowrated")
    finally:
        controller.read_low_rated = original

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert [review["rating"] for review in response.json()] == [1, 2]
