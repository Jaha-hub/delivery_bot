from typing import Union

from aiogram.utils.keyboard import InlineKeyboardBuilder

from models.category import Category
from models.product import Product


def menu_keyboard(objs: Union[list[Category], list[Product]], lang:str):
    keyboard = InlineKeyboardBuilder()
    for obj in objs:
        keyboard.button(text=obj.name, callback_data=str(obj.id))
    keyboard.button(text="Корзина", callback_data="cart")
    keyboard.button(text="Назад", callback_data="back")

    keyboard.adjust(2)
    return keyboard.as_markup()

def product_keyboard( lang:str,quantity: int = 1):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="➖", callback_data="minus")
    keyboard.button(text=str(quantity), callback_data=str(quantity))
    keyboard.button(text="➕", callback_data="plus")

    keyboard.button(text="1❌", callback_data="delete1")
    keyboard.button(text="2❌", callback_data="delete2")

    keyboard.button(text="Добавить в корзину", callback_data="add_cart")
    keyboard.button(text="Назад", callback_data="back")

    keyboard.adjust(3,2,1)
    return keyboard.as_markup()