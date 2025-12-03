from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

def cart_keyboard(products):
    keyboard = InlineKeyboardBuilder()
    for i in range(len(products)):
        keyboard.button(text=f"{i+1}", callback_data=f"remove_{products[i].id}")
    keyboard.adjust(5)
    keyboard.row(
        InlineKeyboardButton(text="Сделать Заказ", callback_data="order")
    )
    keyboard.row(
        InlineKeyboardButton(text="Назад", callback_data="back")
    )
    return keyboard.as_markup()