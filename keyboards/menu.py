from typing import Union


from aiogram.utils.keyboard import InlineKeyboardBuilder

from models.category import Category
from models.product import Product


def menu_keyboard(
     objs : Union[list[Category], list[Product]],
     lang: str,
):
    kb = InlineKeyboardBuilder()
    for obj in objs:
        kb.button(text=obj.name, callback_data=str(obj.id))

    kb.button(text="Корзина", callback_data="cart")
    kb.button(text="Назад", callback_data="back")

    kb.adjust(2)
    return kb.as_markup()
