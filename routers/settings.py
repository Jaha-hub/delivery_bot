from aiogram import Router, F

from keyboards.settings import setting_kb

router = Router()


@router.callback_query(F.data == "settings")
async def settings(callback_data):
    await callback_data.answer(text="какой язык вы хотите выбрать", reply_markup=setting_kb)
