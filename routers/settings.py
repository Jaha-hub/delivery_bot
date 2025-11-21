from aiogram import Router, F

from keyboards.settings import setting_kb
from aiogram.types import CallbackQuery, message

router = Router()


@router.callback_query(F.data == "settings")
async def settings(callback: CallbackQuery):
    await callback.message.answer(text="какой язык вы хотите выбрать", inline_keyboard=[setting_kb()],reply_markup=setting_kb())
