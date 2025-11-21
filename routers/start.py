from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.start import start_kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Здраствуйте", reply_markup=start_kb())
