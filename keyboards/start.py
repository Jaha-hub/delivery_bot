from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="заказать", callback_data="order")
    kb.button(text="история", callback_data="history")
    kb.button(text="настройки", callback_data="settings")
    kb.adjust(1, 2)
    return kb.as_markup()
