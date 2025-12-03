from config import async_session
from managers.product import ProductManager


async def get_cart_products_text(cart):
    products = []
    async with async_session() as session:
        manager = ProductManager(session)
        for product_id in cart.keys():
            product = await manager.get(int(product_id))
            products.append(product)
    text = "Ваша Корзина\n"
    total = 0
    i = 1
    for product in products:
        total += product.price * cart[str(product.id)]
        text += f"\n{i}. {product.name} x {cart[str(product.id)]}={round(product.price, 2) * cart[str(product.id)]}"
        i += 1
    text += f"\n\nИтого: {round(total, 2)}"
    return text, products