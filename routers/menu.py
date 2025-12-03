from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import async_session
from keyboards.menu import menu_keyboard, product_keyboard
from keyboards.start import start_kb
from managers.category import CategoryManager
from managers.product import ProductManager
from models.user import User
from services.cart import CartService
from states.menu import MenuForm

router = Router()


@router.callback_query(F.data == "menu")
async def menu(cb: CallbackQuery, user: User, state: FSMContext):
    print()
    async with async_session() as session:
        manager = CategoryManager(session)
        category = await manager.list()

    await cb.message.edit_text(
        "Выберите категорию",
        reply_markup=menu_keyboard(category, user.language)
    )
    await state.set_state(MenuForm.category)


@router.callback_query(F.data == "cart")
async def cart(cb: CallbackQuery, user: User, state: FSMContext):
    pass


@router.callback_query(F.data.isdigit(), MenuForm.category)
async def menu(cb: CallbackQuery, user: User, state: FSMContext):
    category_id = int(cb.data)
    async with async_session() as session:
        category_manager = CategoryManager(session)
        category = await category_manager.get(category_id)
        if category is None:
            await cb.answer("Категории нет")
            return None
        product_manager = ProductManager(session)
        products = await product_manager.list(category_id)
    await state.update_data(
        category_id=category_id,
    )
    await cb.message.edit_text(
        "Выберите продукты",
        reply_markup=menu_keyboard(products, user.language)
    )
    await state.set_state(MenuForm.product)
    return None


@router.callback_query(F.data == "back", MenuForm.product)
async def back(cb: CallbackQuery, user: User, state: FSMContext):
    async with async_session() as session:
        manager = CategoryManager(session)
        category = await manager.list()

    await cb.message.edit_text(
        "Выберите категорию",
        reply_markup=menu_keyboard(category, user.language)
    )
    await state.set_state(MenuForm.product)


@router.callback_query(F.data.isdigit(), MenuForm.product)
async def menu(cb: CallbackQuery, user: User, state: FSMContext):
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
            reply_markup=product_keyboard(user.language)
        )
        await state.update_data(product=product.id, quantity=1)

        await state.set_state(MenuForm.quantity)
        return None


@router.callback_query(F.data == "back", MenuForm.quantity)
async def menu(cb: CallbackQuery, user: User, state: FSMContext):
    data = await state.get_data()
    category_id = int(data["category_id"])
    await cb.message.delete()
    async with async_session() as session:
        category_manager = CategoryManager(session)
        category = await category_manager.get(category_id)
        if category is None:
            await cb.answer("Категории нет")
            await cb.message.answer("Выберите Действия", reply_markup=start_kb(user.language))
            return None
        product_manager = ProductManager(session)
        products = await product_manager.list(category_id)
    await state.update_data(
        category_id=category_id,
    )
    await cb.message.answer(
        "Выберите продукты",
        reply_markup=menu_keyboard(products, user.language)
    )
    await state.set_state(MenuForm.product)
    return None


@router.callback_query(F.data == "plus", MenuForm.quantity)
async def menu(cb: CallbackQuery, user: User, state: FSMContext):
    data = await state.get_data()
    quantity = data["quantity"]
    quantity += 1
    await cb.message.edit_reply_markup(
        reply_markup=product_keyboard(user.language, quantity)
    )
    await state.update_data(quantity=quantity)
    await state.set_state(MenuForm.quantity)


@router.callback_query(F.data == "minus", MenuForm.quantity)
async def menu(cb: CallbackQuery, user: User, state: FSMContext):
    data = await state.get_data()
    quantity = data["quantity"]
    if quantity <= 1:
        return None
    quantity -= 1
    await cb.message.edit_reply_markup(
        reply_markup=product_keyboard(user.language, quantity)
    )
    await state.update_data(quantity=quantity)
    await state.set_state(MenuForm.quantity)
    return None


@router.callback_query(F.data.isdigit(), MenuForm.quantity)
async def menu(cb: CallbackQuery, user: User, state: FSMContext):
    await cb.answer(cb.data)


@router.callback_query(F.data == "add_cart", MenuForm.quantity)
async def add_cart(cb: CallbackQuery, user: User, state: FSMContext):
    cart_servis = CartService()
    data = await state.get_data()
    await cart_servis.add_to_cart(
        user.id,
        data["product"],
        data["quantity"]
    )
    cart = await cart_servis.get_cart(user.id)
    print(cart)

    await state.clear()
    await cb.message.delete()
    await cb.answer("Добавлено")
    async with async_session() as session:
        manager = CategoryManager(session)
        category = await manager.list()

    await cb.message.answer(
        "Выберите категорию",
        reply_markup=menu_keyboard(category, user.language)
    )
    await state.set_state(MenuForm.category)



@router.callback_query(F.data == "delete1", MenuForm.product)
async def delete_first_product(
        cb: CallbackQuery,
        state: FSMContext,
        user: User
):
    async with async_session() as session:
        manager = ProductManager(session)
        data = await manager.get(0)
        manager.remove_from_cart(
            user.id,
            data["product"],
            data["quantity"],
        )


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
        await cb.message.answer("Ваша корзина пустая")
        return None
    products = []
    async with async_session() as session:
        manager = ProductManager(session)
        for product_id in cart.keys():
            product = await manager.get(int(product_id))
            products.append(product)
        text = "Ваша корзина\n"
        total = 0
        i = 1
        for product in products:
            total += product.price * cart[str(product_id)]
            text += f"\n {product.name} x {cart[str(product.id)]} {round(product.price, 2)}"
            i +=1
        await cb.message.answer(text)
        return None