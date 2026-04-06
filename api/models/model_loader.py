from . import ingredients, menu_item_ingredients, menu_items, order_items, orders, promo_codes, reviews
from ..dependencies.database import engine

def index():
    ingredients.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    menu_item_ingredients.Base.metadata.create_all(engine)
    orders.Base.metadata.create_all(engine)
    order_items.Base.metadata.create_all(engine)
    promo_codes.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)