from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from config import TOKEN
from middlewares.logging import LoggingMiddleware
from middlewares.auth import AuthMiddleware

bot = Bot(TOKEN)
dp = Dispatcher()

dp.update.middleware(LoggingMiddleware())
dp.update.middleware(AuthMiddleware())


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello")

async def main():
    await dp.start_polling(bot)
