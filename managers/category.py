from sqlalchemy import insert, select, update,delete
from sqlalchemy.ext.asyncio import AsyncSession
from unicodedata import category

from models.category import Category


class CategoryManager:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def create(
            self,
            category_id: int,
            name: str,
    ):
        stmt = insert(Category).values(
            id=category_id,
            name=name,
        )
        await self.db.execute(stmt)
        await self.db.commit()
    async def get(
            self,
            category_id: int,
    ):
        stmt = select(Category).where(category_id == category_id)
        result = await self.db.execute(stmt)
        print(result)
        return result.scalar_one_or_none()

    async def list(self):
        stmt = select(Category)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(
            self, category_id: int
    ):
        stmt = update(Category).where(category_id == category_id)
        await self.db.execute(stmt)
        await self.db.commit()

    async def delete(self, category_id: int):
        stmt = delete(Category).where(category_id == category_id)
        await self.db.execute(stmt)
        await self.db.commit()