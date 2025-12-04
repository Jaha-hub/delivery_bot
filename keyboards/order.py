from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def contact_kb(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Поделиться контактом", request_contact=True)
    keyboard.button(text="Назад")
    keyboard.adjust(1,1)
    return keyboard.as_markup(
        resize_keyboard=True,
    )

def location_keyboard(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="поделитесь местоположением", request_location=True)
    keyboard.button(text="Назад")
    keyboard.adjust(1,1)
    return keyboard.as_markup(
        resize_keyboard=True,
    )

def comment_kb(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Пропустить")
    keyboard.button(text="Назад")
    keyboard.adjust(1,1)
    return keyboard.as_markup(
        resize_keyboard=True,
    )

def confirm_kb(lang):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="нет", callback_data="back")
    keyboard.button(text="Да", callback_data="yes")
    keyboard.adjust(2)
    return keyboard.as_markup()