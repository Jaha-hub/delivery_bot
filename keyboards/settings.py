from aiogram.utils.keyboard import InlineKeyboardBuilder

def settings_keyboard(lang):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Смена Имени", callback_data="fullname")
    keyboard.button(text="Смена Языка", callback_data="language")
    keyboard.button(text="Назад", callback_data="back")

    keyboard.adjust(2,1)

    return keyboard.as_markup()

def language_keyboard(lang):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="🇷🇺", callback_data="lang_ru")
    keyboard.button(text="🇬🇧", callback_data="lang_en")
    keyboard.button(text="🇺🇿", callback_data="lang_uz")

    keyboard.button(text="назад", callback_data="back")

    keyboard.adjust(3,1)

    return keyboard.as_markup()
