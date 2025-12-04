from aiogram.fsm.state import State, StatesGroup

class OrderForm(StatesGroup):
    phone_number = State()
    location = State()
    comment = State()
    confirm = State()