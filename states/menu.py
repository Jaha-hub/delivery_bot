from aiogram.fsm.state import State, StatesGroup

class MenuForm(StatesGroup):
    category = State()
    product = State()
    quantity = State()