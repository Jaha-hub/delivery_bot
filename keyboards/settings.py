from aiogram.utils.keyboard import InlineKeyboardBuilder


def setting_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="ru", callback_data="change_lang_to_ru")
    kb.button(text="en", callback_data="change_lang_to_en")
    kb.button(text="назад", callback_data="get_back")
    kb.adjust(1,1)
    return kb.as_markup()