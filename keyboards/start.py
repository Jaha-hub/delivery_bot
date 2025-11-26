from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_kb(lang):
    kb = InlineKeyboardBuilder()
    kb.button(text="заказать", callback_data="menu")
    kb.button(text="история заказов", callback_data="history")
    kb.button(text="о нас", callback_data="about")
    kb.button(text="настройки", callback_data="settings")
    kb.adjust(1, 3)
    return kb.as_markup()

def back_keyboard(lang):
    kb = InlineKeyboardBuilder()

    kb.button(
        text="Назад", callback_data="back",
    )

    return kb.as_markup()