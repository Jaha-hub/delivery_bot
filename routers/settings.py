from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import async_session
from keyboards.settings import settings_keyboard, language_keyboard
from keyboards.start import back_keyboard, start_keyboard

from managers.user import UserManager

from models.user import User

from states.settings import LanguageForm, FullnameForm

router = Router()


@router.callback_query(F.data == "settings")
async def settings_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    await cb.message.edit_text(
        "Выберите Действие",
        reply_markup=settings_keyboard(user.language)
    )


@router.callback_query(F.data == "fullname")
async def fullname_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    await cb.message.edit_text(
        "Напишите новое ФИО",
        reply_markup=back_keyboard(user.language)
    )
    await state.set_state(FullnameForm.fullname)
    await state.update_data(message_id=cb.message.message_id)


@router.callback_query(F.data == "back", FullnameForm.fullname)
async def back_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    await state.clear()
    await cb.message.edit_text(
        "Выберите Действие",
        reply_markup=settings_keyboard(user.language)
    )

@router.message(F.text, FullnameForm.fullname)
async def get_fullname_handler(
        message: Message,
        state: FSMContext,
        user: User
):
    async with async_session() as session:
        manager = UserManager(session)
        await manager.update_fullname(
            user.id,
            message.text
        )
    await message.delete()
    data = await state.get_data()
    await state.clear()
    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["message_id"],
        text="Успешно Изменили Имя\nВыберите Действие",
        reply_markup=start_keyboard(user.language)
    )
@router.callback_query(F.data == "language")
async def language_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    await cb.message.edit_text(
        "Выберите Язык",
        reply_markup=language_keyboard(user.language)
    )
    await state.set_state(LanguageForm.language)
    await state.update_data(message_id=cb.message.message_id)

@router.callback_query(F.data == "back", LanguageForm.language)
async def back_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    await state.clear()
    await cb.message.edit_text(
        "Выберите Действие",
        reply_markup=settings_keyboard(user.language)
    )

@router.callback_query(F.data.startswith("lang_"), LanguageForm.language)
async def lang_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    await cb.answer("Успешно поменяли язык")
    t, lang = cb.data.split("_")

    async with async_session() as session:
        manager = UserManager(session)
        await manager.update_language(
            user.id,
            lang
        )
        user = await manager.get(
            user.id
        )
    await state.clear()
    await cb.message.edit_text(
        "Выберите Действие",
        reply_markup=start_keyboard(user.language)
    )