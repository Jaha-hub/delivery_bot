from aiogram import Bot, Dispatcher
from config import TOKEN
from routers.start import router as start
from routers.settings import router as settings
bot = Bot(TOKEN)
dp = Dispatcher()


dp.include_router(start)
dp.include_router(settings)

async def main():
    await dp.start_polling(bot)
