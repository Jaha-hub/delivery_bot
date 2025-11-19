import asyncio

from config import async_session

from managers.user import UserManager


async def main():
    async with async_session() as session:
        manager = UserManager(session)
        user = await manager.get(
            123,
        )
        print(user)
if __name__ == "__main__":
    asyncio.run(main())