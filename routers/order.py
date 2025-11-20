from aiogram import Router,F
from aiogram.types import Message, CallbackQuery

from keyboards.order import order_kb

router = Router()


@router.callback_query(F.data =="order")
async def order_handler(call: CallbackQuery):
    await call.answer("что вы хотите заказать", reply_markup=order_kb(lang="ru"))