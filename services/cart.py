from redis import asyncio as redis
import json

class CartService:
    def __init__(self):
        self.redis = redis.from_url("redis://localhost:6379", )

    async def get_cart(self,user_id):
        cart = await self.redis.get(f"cart:{user_id}")
        if not cart:
            await self.redis.set(
                f"cart:{user_id}",
                json.dumps({})
            )
            return {}
        return json.loads(cart)
    async def add_to_cart(
            self,
            user_id: int,
            product_id: int,
            quantity: int,
    ):
        # key and value
        # {"cart:user_id": {product_id:quantity}
        # {"user_id:product_id": quantity}
        # {"1234:1": 3, "1234:2":5}
        cart = await self.get_cart(user_id)  # 5
        if str(product_id) in cart:
            cart[str(product_id)] += quantity
        else:
            cart[str(product_id)] = quantity

            await self.redis.set(
                f"cart:{user_id}",
                json.dumps(cart)
            )

    async def remove_from_cart(
            self,
            user_id: int,
            product_id: int,
    ):
        cart = await self.get_cart(user_id)  # 5
        if str(product_id) in cart:
            cart.pop(str(product_id))
        await self.redis.get(
            f"cart:{user_id}",
            json.dumps(cart)
        )

    async def clear_cart(
            self,
            user_id: int,
    ):
        cart = await self.get_cart(user_id)
        cart.clear()
        await self.redis.set(
            f"cart:{user_id}",
            json.dumps(cart)
        )
