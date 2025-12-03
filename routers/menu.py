from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import async_session
from keyboards.cart import cart_keyboard
from keyboards.menu import menu_keyboard, product_keyboard
from keyboards.start import start_keyboard
from managers.category import CategoryManager
from managers.product import ProductManager
from models.user import User
from services.cart import CartService
from states.menu import MenuForm
from utils.cart import get_cart_products_text

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
        "Выберите Категорию",
        reply_markup=menu_keyboard(
            categories,
            user.language
        )
    )
    await state.set_state(MenuForm.category)


@router.callback_query(F.data == "cart")
async def cart_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    cart_service = CartService()
    cart = await cart_service.get_cart(user.id)
    await cb.message.delete()
    await state.clear()
    if len(cart.keys()) == 0:
        # Кнопка назад
        await cb.message.answer("Ваша Корзина Пустая")
        return None
    text, products = await get_cart_products_text(cart)
    await cb.message.answer(text, reply_markup=cart_keyboard(products))
    return None

@router.callback_query(F.data.startswith("remove_"))
async def remove_cart_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    cart_service = CartService()
    t, product_id = cb.data.split("_")
    await cart_service.remove_from_cart(user.id, int(product_id))
    cart = await cart_service.get_cart(user.id)
    await cb.message.delete()
    await state.clear()
    if len(cart.keys()) == 0:
        # Кнопка назад
        await cb.message.answer("Ваша Корзина Пустая")
        return None
    text, products = await get_cart_products_text(cart)
    await cb.message.answer(text, reply_markup=cart_keyboard(products))
    return None

@router.callback_query(F.data.isdigit(), MenuForm.category)
async def category_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    category_id = int(cb.data)
    async with async_session() as session:
        category_manager = CategoryManager(session)
        category = await category_manager.get(category_id)
        if category is None:
            await cb.answer("Категории Нету")
            return None
        product_manager = ProductManager(session)
        products = await product_manager.list(category_id)
    await state.update_data(
        category=category_id
    )
    await cb.message.edit_text(
        "Выберите Продукт",
        reply_markup=menu_keyboard(
            products,
            user.language
        )
    )
    await state.set_state(MenuForm.product)
    return None


@router.callback_query(F.data == "back", MenuForm.product)
async def back_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    async with async_session() as session:
        manager = CategoryManager(session)
        categories = await manager.list()

    await cb.message.edit_text(
        "Выберите Категорию",
        reply_markup=menu_keyboard(
            categories,
            user.language
        )
    )
    await state.set_state(MenuForm.category)


@router.callback_query(F.data.isdigit(), MenuForm.product)
async def product_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    product_id = int(cb.data)
    async with async_session() as session:
        product_manager = ProductManager(session)
        product = await product_manager.get(product_id)
        if product is None:
            return None
        await cb.message.delete()
        await cb.message.answer_photo(
            product.photo,
            caption=f"<b>{product.name}</b>\n\n{product.description}\n{product.price} сум",
            reply_markup=product_keyboard()
        )
        await state.update_data(product=product.id, quantity=1)
        await state.set_state(MenuForm.quantity)
        return None


@router.callback_query(F.data == "back", MenuForm.quantity)
async def back_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    data = await state.get_data()
    category_id = int(data["category"])
    await cb.message.delete()
    async with async_session() as session:
        category_manager = CategoryManager(session)
        category = await category_manager.get(category_id)
        if category is None:
            await cb.answer("Категории Нету")
            await cb.message.answer(
                "Выберите Действие",
                reply_markup=start_keyboard(user.language)
            )
            await state.clear()
            return None
        product_manager = ProductManager(session)
        products = await product_manager.list(category_id)
    await state.update_data(
        category=category_id
    )
    await cb.message.answer(
        "Выберите Продукт",
        reply_markup=menu_keyboard(
            products,
            user.language
        )
    )
    await state.set_state(MenuForm.product)
    return None


@router.callback_query(F.data == "plus", MenuForm.quantity)
async def plus_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    data = await state.get_data()
    quantity = data["quantity"]
    quantity += 1
    await cb.message.edit_reply_markup(
        reply_markup=product_keyboard(
            quantity
        )
    )
    await state.update_data(quantity=quantity)
    await state.set_state(MenuForm.quantity)


@router.callback_query(F.data == "minus", MenuForm.quantity)
async def minus_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    data = await state.get_data()
    quantity = data["quantity"]
    quantity -= 1 if quantity > 1 else 1
    await cb.message.edit_reply_markup(
        reply_markup=product_keyboard(
            quantity
        )
    )
    await state.update_data(quantity=quantity)
    await state.set_state(MenuForm.quantity)


@router.callback_query(F.data.isdigit(), MenuForm.quantity)
async def quantity_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    await cb.answer(cb.data)


@router.callback_query(F.data == "add_cart", MenuForm.quantity)
async def add_cart_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    cart_service = CartService()
    data = await state.get_data()
    await cart_service.add_to_cart(
        user.id,
        data["product"],
        data["quantity"]
    )

    await state.clear()
    await cb.message.delete()
    await cb.answer("Добавили в корзину")

    async with async_session() as session:
        manager = CategoryManager(session)
        categories = await manager.list()

    await cb.message.answer(
        "Выберите Категорию",
        reply_markup=menu_keyboard(
            categories,
            user.language
        )
    )
    await state.set_state(MenuForm.category)
