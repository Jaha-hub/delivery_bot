from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Product


class ProductManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
            self,
            category_id: int,
            name: str,
            description: str,
            price: float,
            photo: str,
    ):
        stmt = insert(Product).values(
            name=name,
            description=description,
            price=price,
            photo=photo,
            category_id=category_id,
        )
        await self.db.execute(stmt)
        await self.db.commit()

    async def get(
            self,
            product_id:int,
    ):
        stmt = select(Product).where(Product.id == product_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self):
        stmt = select(Product)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(
            self, product_id: int, price:float, description: str
    ):
        stmt = update(Product).where(Product.id == product_id).values(price=price,description=description)
        await self.db.execute(stmt)
        await self.db.commit()

    async def delete(self, product_id: int):
        stmt = delete(Product).where(Product.id == product_id)
        await self.db.execute(stmt)
        await self.db.commit()