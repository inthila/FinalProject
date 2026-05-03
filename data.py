from api.dependencies.database import SessionLocal
from api.models.ingredients import Ingredient
from api.models.low_stocks_alerts import LowStocksAlert
from api.models.menu_items import MenuItem
from api.models.menu_item_ingredients import MenuItemIngredient
from api.models.orders import Order
from api.models.order_items import OrderItem
from api.models.promo_codes import PromoCode
from api.models.reviews import Review
from api.models import model_loader
from datetime import date
import uuid

model_loader.index()

db = SessionLocal()

flour = Ingredient(name="Flour", quantity=100.0, unit="g", low_stock_threshold=10.0)
tomato = Ingredient(name="Tomato Sauce", quantity=5.0, unit="oz", low_stock_threshold=2.0)
cheese = Ingredient(name="Cheese", quantity=0.5, unit="oz", low_stock_threshold=1.0)
chicken = Ingredient(name="Chicken", quantity=200.0, unit="g", low_stock_threshold=50.0)
cream = Ingredient(name="Heavy Cream", quantity=50.0, unit="ml", low_stock_threshold=10.0)
db.add_all([flour, tomato, cheese, chicken, cream])
db.commit()

alert1 = LowStocksAlert(ingredient_id=cheese.id, quantity_at_alert=0.5, threshold_at_alert=1.0, is_active=True)
db.add(alert1)
db.commit()

promo1 = PromoCode(code="SAVE10", discount_percent=10.00, expiration_date=date(2025, 12, 31), is_active=True)
promo2 = PromoCode(code="HALFOFF", discount_percent=50.00, expiration_date=date(2026, 1, 1), is_active=False)
promo3 = PromoCode(code="WELCOME5", discount_percent=5.00, expiration_date=date(2026, 12, 31), is_active=True)
db.add_all([promo1, promo2, promo3])
db.commit()

pizza = MenuItem(name="Margherita Pizza", description="Classic tomato and cheese pizza", price=12.99, calories=800, category="Pizza", is_available=True)
pasta = MenuItem(name="Pasta Alfredo", description="Creamy alfredo pasta", price=10.99, calories=950, category="Pasta", is_available=True)
burger = MenuItem(name="Chicken Burger", description="Grilled chicken burger", price=9.99, calories=650, category="Burger", is_available=True)
salad = MenuItem(name="Caesar Salad", description="Fresh romaine with caesar dressing", price=7.99, calories=400, category="Salad", is_available=False)
db.add_all([pizza, pasta, burger, salad])
db.commit()

db.add_all([
    MenuItemIngredient(menu_item_id=pizza.id, ingredient_id=flour.id, quantity_required=50.0),
    MenuItemIngredient(menu_item_id=pizza.id, ingredient_id=tomato.id, quantity_required=3.0),
    MenuItemIngredient(menu_item_id=pizza.id, ingredient_id=cheese.id, quantity_required=2.0),
    MenuItemIngredient(menu_item_id=pasta.id, ingredient_id=flour.id, quantity_required=30.0),
    MenuItemIngredient(menu_item_id=pasta.id, ingredient_id=cream.id, quantity_required=20.0),
    MenuItemIngredient(menu_item_id=burger.id, ingredient_id=chicken.id, quantity_required=150.0),
])
db.commit()

order1 = Order(tracking_number=str(uuid.uuid4())[:8].upper(), customer_name="Jane Doe", customer_phone="704-555-0101", customer_address="123 Main St, Charlotte, NC", order_type="delivery", status="pending", payment_method="credit_card", total_price=10.99, promo_code_id=None)
order2 = Order(tracking_number=str(uuid.uuid4())[:8].upper(), customer_name="John Smith", customer_phone="704-555-0202", customer_address=None, order_type="takeout", status="completed", payment_method="cash", total_price=17.99, promo_code_id=promo1.id)
db.add_all([order1, order2])
db.commit()

oi1 = OrderItem(order_id=order1.id, menu_item_id=pasta.id, quantity=1, special_instructions="No pepper")
oi2 = OrderItem(order_id=order2.id, menu_item_id=burger.id, quantity=1, special_instructions=None)
oi3 = OrderItem(order_id=order2.id, menu_item_id=pasta.id, quantity=1, special_instructions="Extra cream")
db.add_all([oi1, oi2, oi3])
db.commit()

review1 = Review(order_item_id=oi1.id, rating=5, comment="Absolutely delicious!")
review2 = Review(order_item_id=oi2.id, rating=4, comment="Great burger, a bit salty.")
db.add_all([review1, review2])
db.commit()

db.close()
print("Data added.")
