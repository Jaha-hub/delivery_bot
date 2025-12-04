from aiogram import Bot, Dispatcher

from config import TOKEN

from middlewares.auth import AuthMiddleware
from middlewares.logging import LoggingMiddleware

from routers.start import router as start
from routers.settings import router as settings
from routers.menu import router as menu
from routers.order_form import router as order
bot = Bot(TOKEN)
dp = Dispatcher()

dp.update.middleware(LoggingMiddleware())
dp.update.middleware(AuthMiddleware())

dp.include_router(menu)
dp.include_router(order)
dp.include_router(start)
dp.include_router(settings)
