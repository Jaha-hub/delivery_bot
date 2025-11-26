from aiogram.fsm.state import State, StatesGroup

class FullnameForm(StatesGroup):
    fullname = State()

class LanguageForm(StatesGroup):
    language = State()