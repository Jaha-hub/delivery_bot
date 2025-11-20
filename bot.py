from aiogram import Bot, Dispatcher
from config import TOKEN
from middlewares.logging import LoggingMiddleware
from middlewares.auth import AuthMiddleware
from routers.start import router as start
from routers.order import router as order
bot = Bot(TOKEN)
dp = Dispatcher()

dp.update.middleware(LoggingMiddleware())
dp.update.middleware(AuthMiddleware())
dp.include_router(start)
dp.include_router(order)

async def main():
    await dp.start_polling(bot)
