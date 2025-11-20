from sqlalchemy import insert, select, update,delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserCreate


class UserManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
            self,
            user_id: int,
            full_name: str,
    ):
        # INSERT INTO TABLE(COLUMNS) VALUES
        # Запрос для БД
        # Insert(Модельку).values(столбец=значение)
        stmt = insert(User).values(
            id=user_id,
            full_name=full_name,
        ).returning(User)
        # execute запускает наше утверждение
        result = await self.db.execute(stmt)
        # commit Сохраняет в БД наше утверждение
        await self.db.commit()
        return result.scalar_one_or_none()

    async def get(
            self,
            user_id: int,
    ):
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        print(result)
        # достань первое или ничего
        return result.scalar_one_or_none()

    async def list(self):
        stmt = select(User)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(
            self, user_id: int, language: str
    ):
        stmt = update(User).where(User.id == user_id).values(Language=language)
        await self.db.execute(stmt)
        await self.db.commit()

    async def delete(self, user_id: int):
        stmt = delete(User).where(User.id == user_id)
        await self.db.execute(stmt)
        await self.db.commit()

    async def get_or_create(
            self,
            user_id: int,
            full_name: str,
    ):
        user = await self.get(user_id)
        if user is None:
            user = await self.create(user_id, full_name)
        return user