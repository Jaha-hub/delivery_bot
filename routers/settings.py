from aiogram import Router, F

from config import async_session
from keyboards.settings import setting_kb
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from managers.user import UserManager
from keyboards.start import back_keyboard, start_kb
from models.user import User
from states.settings import LanguageForm, FullnameForm
from keyboards.settings import language_kb
router = Router()


@router.callback_query(F.data == "settings")
async def settings(
        cb: CallbackQuery,
        state: FSMContext,
        user: User,
):
    await cb.message.edit_text(
        text="Выберите действие",
        reply_markup=setting_kb(user.language)
    )


@router.callback_query(F.data == "change_name")
async def fullname_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User,
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
        user: User,
):
    await state.clear()
    await cb.message.edit_text(
        "Выберите действие",
        reply_markup=back_keyboard(user.language)
    )


@router.message(F.text, FullnameForm.fullname)
async def get_fullname_handler(
        message: Message,
        state: FSMContext,
        user: User,
):
    async with async_session() as session:
        manager = UserManager(session)
        await manager.update_fullname(
            user.id,
            message.text
        )
    # Логика обновления
    await message.delete()
    data = await state.get_data()
    await state.clear()
    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["message_id"],
        text="Успешно изменили имя \n Выберите действие",
        reply_markup=start_kb(user.language)
    )




@router.callback_query(F.data == "change_lang")
async def language_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User,
):
    await cb.message.edit_text(
        "Выберите язык",
        reply_markup=language_kb(user.language)
    )
    await state.set_state(LanguageForm.language)
    await state.update_data(message_id=cb.message.message_id)


@router.callback_query(F.data == "back", LanguageForm.language)
async def back_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User,
):
    await state.clear()
    await cb.message.edit_text(
        "Выберите действие",
        reply_markup=back_keyboard(user.language)
    )

@router.callback_query(F.data.startswith("lang_"), LanguageForm.language)
async def language_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User,
):
    await cb.answer("Успешно поменяли язык")
    t,lang = cb.data.split("_")
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
        "Выберите текст",
        reply_markup=start_kb(user.language)
    )