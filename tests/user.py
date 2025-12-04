import asyncio

from config import async_session
from managers.order import OrderManager

from managers.user import UserManager

async def main():
    async with async_session() as session:
        manager = OrderManager(session)
        orders = await manager.list(1724283740)
        for order in orders:
            for product in order.products:
                print(product.product.name)


if __name__ == "__main__":
    asyncio.run(main())