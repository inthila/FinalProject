from . import ingredients, menu_item_ingredients, menu_items, order_items, orders, promo_codes, reviews


def load_routes(app):
    app.include_router(ingredients.router)
    app.include_router(menu_item_ingredients.router)
    app.include_router(menu_items.router)
    app.include_router(order_items.router)
    app.include_router(orders.router)
    app.include_router(promo_codes.router)
    app.include_router(reviews.router)
