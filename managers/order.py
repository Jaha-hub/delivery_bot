from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.order import Order,OrderProduct

class OrderManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
            self,
            phone_number: str,
            client_id: int,
            latitude: float,
            longitude: float,
            total_price: float,
            comment: str | None,
            products: dict,
    ):
        #Транзакция
            stmt = insert(Order).values(
                phone_number=phone_number,
                client_id=client_id,
                latitude=latitude,
                longitude=longitude,
                total_price=total_price,
                comment=comment,
            ).returning(Order.id)
            result = await self.db.execute(stmt)
            order_id =  result.fetchone()[0]
            for product_id , quantity in products.items():
                stmt = insert(OrderProduct).values(
                    order_id=order_id,
                    product_id=int(product_id),
                    quantity=quantity,
                )
                await self.db.execute(stmt)
            await self.db.commit()
            return order_id

    async def list(self, client_id:int):
        stmt = select(Order).where(Order.client_id == client_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()