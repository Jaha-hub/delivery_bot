from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Product


class ProductManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(
            self,
            product_id:int,
    ):
        stmt = select(Product).where(Product.id == product_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self, category_id: int):
        stmt = select(Product).where(Product.category_id == category_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()
