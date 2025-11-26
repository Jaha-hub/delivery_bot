from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


from config import async_session
from keyboards.menu import menu_keyboard
from managers.category import CategoryManager
from managers.product import ProductManager
from models.category import Category
from models.user import User
from states.menu import MenuForm
router = Router()


@router.callback_query(F.data == "menu")
async def menu_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    async with async_session() as session:
        manager = CategoryManager(session)
        categories = await manager.list()

    await cb.message.edit_text(
        "Выберите категорию",
        reply_markup=menu_keyboard(
            categories,
            user.language,
        )
    )
    await state.set_state(MenuForm.category)

@router.callback_query(F.data == "cart")
async def cart_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    pass

@router.callback_query(F.data.isdigit(), MenuForm.category)
async def category_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    category_id = int(cb.data)
    async with async_session() as session:
        category_manager = CategoryManager(session)
        category =  category_manager.get(category_id)
        if category is None:
            await cb.answer("такой категории нету")
            return None
        product_manager = ProductManager(session)
        products = await product_manager.list(category_id)
    await state.update_data(
        category=category_id
    )
    await cb.message.edit_text(
        "Выберите Продукты",
        reply_markup=menu_keyboard(
            products,
            user.language,
        )
    )
    await state.set_state(MenuForm.product)
    return None
