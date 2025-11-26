from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.settings import setting_kb
from keyboards.start import start_kb
from models.user import User

router = Router()


@router.message(CommandStart())
async def start(message: Message, user: User, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет я интернет магазин \n Выберите действие",
                         reply_markup=start_kb(user.language
                                                )
    )


@router.callback_query(F.data == "back")
async def back(cb, user: User, state: FSMContext):
    await state.clear()
    await cb.message.edit_text(
        "Выберите Действие",
        reply_markup=start_kb(user.language)
    )
