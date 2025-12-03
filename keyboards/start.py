from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_keyboard(lang):
    kb = InlineKeyboardBuilder()
    kb.button(text="Заказать", callback_data="menu")
    kb.button(text="История Заказов", callback_data="history")
    kb.button(text="О Нас", callback_data="about")
    kb.button(text="Настройки", callback_data="settings")
    kb.adjust(1, 3)
    return kb.as_markup()

def back_keyboard(lang):
    kb = InlineKeyboardBuilder()

    kb.button(
        text="Назад", callback_data="back"
    )

    return kb.as_markup()