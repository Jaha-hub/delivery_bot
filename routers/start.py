from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.start import start_keyboard
from models.user import User

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, user: User, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет я Интернет Магазин\nВыберите Действие",
        reply_markup=start_keyboard(user.language)
    )

@router.callback_query(F.data == "back")
async def back_handler(cb: CallbackQuery, state: FSMContext, user: User):
    await state.clear()
    await cb.message.edit_text(
        "Выберите Действие",
        reply_markup=start_keyboard(user.language)
    )