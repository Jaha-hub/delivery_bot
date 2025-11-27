from aiogram import Bot, Dispatcher
from config import TOKEN
from managers import user
from middlewares.logging import LoggingMiddleware
from middlewares.auth import AuthMiddleware
from routers.settings import router as settings
from routers.start import router as start
from routers.order import router as order
from routers.menu import router as menu

bot = Bot(TOKEN)
dp = Dispatcher()

dp.update.middleware(LoggingMiddleware())
dp.update.middleware(AuthMiddleware())

dp.include_router(menu)
dp.include_router(start)
dp.include_router(order)
dp.include_router(settings)


async def main():
    await dp.start_polling(bot)
