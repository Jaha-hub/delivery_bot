from aiogram.utils.keyboard import InlineKeyboardBuilder

def order_kb(lang: str = "ru"):
    kb = InlineKeyboardBuilder()
    kb.button(text="пицца")
    kb.button(text="картошка")
    kb.button(text="бургер")
    kb.adjust(1,2)
    return kb.as_markup()