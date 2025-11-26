from aiogram.utils.keyboard import InlineKeyboardBuilder


def setting_kb(lang):
    kb = InlineKeyboardBuilder()
    kb.button(text="Изменение имени", callback_data="change_name")
    kb.button(text="Изменение языка", callback_data="change_lang")
    kb.button(text="назад", callback_data="back")
    kb.adjust(2,1)
    return kb.as_markup()

def language_kb(lang):
    kb = InlineKeyboardBuilder()

    kb.button(text="🇷🇺", callback_data="lang_ru")
    kb.button(text="🇬🇧", callback_data="lang_en")
    kb.button(text="🇺🇿", callback_data="lang_uz")

    kb.button(text="Назад", callback_data="back")

    kb.adjust(1,3)
    return kb.as_markup()