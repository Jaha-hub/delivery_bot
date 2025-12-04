from itertools import product

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import async_session
from keyboards.order import contact_kb, location_keyboard, comment_kb, confirm_kb
from keyboards.start import start_keyboard
from managers.order import OrderManager
from managers.product import ProductManager
from models.user import User
from services.cart import CartService
from states.order import OrderForm

router = Router()

@router.callback_query(F.data =="order")
async def order_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User,
):
    await cb.message.answer(
        "Поделитесь контактом",
        reply_markup=contact_kb(user.language)
    )
    await state.set_state(OrderForm.phone_number)
@router.message(F.text.lower() == "назад", OrderForm.phone_number)
async def back_handler(
        message: Message,
        state: FSMContext,
        user: User,
):
    await state.clear()
    await message.answer(
        "Выберите Действие",
        reply_markup=start_keyboard(user.language)
    )

@router.message(F.text | F.contact, OrderForm.phone_number)
async def contact_handler(
        message: Message,
        state: FSMContext,
        user: User,
):
    if message.text:
        await state.update_data(
            phone_number=message.text,
        )
    else:
        await state.update_data(
            phone_number=message.contact.phone_number,
        )
    await message.answer(
        "Поделитесь локацией",
        reply_markup=location_keyboard(user.language)
    )
    await state.set_state(OrderForm.location)

@router.message(F.text.lower() == "назад", OrderForm.location)
async def back_handler(
        message: Message,
        state: FSMContext,
        user: User,
):
    pass

@router.message(F.location, OrderForm.location)
async def location_handler(
        message: Message,
        state: FSMContext,
        user: User,
):
    await state.update_data(
        latitude=message.location.latitude,
        longitude=message.location.longitude,
    )
    await message.answer(
        "Хотите написать коментарий",
        reply_markup=comment_kb(user.language)
    )
    await state.set_state(OrderForm.comment)

@router.message(F.text.lower() == "Назад", OrderForm.comment)
async def back_handler(
        message: Message,
        state: FSMContext,
        user: User,
):
    pass



async def get_order_text(
        phone_number,
        comment,
        cart,
        order_id=None,
):
    products = []

    async with async_session() as session:
        manager = ProductManager(session)
        for product_id in cart.keys():
            product = await manager.get(int(product_id))
            products.append(product)
    text = "Ваш Заказ\n" if not order_id else f"Заказ #{order_id}"
    total = 0
    i = 1
    for product in products:
        total += product.price * cart[str(product.id)]
        text += f"\n{i}. {product.name} x {cart[str(product.id)]}={round(product.price, 2) * cart[str(product.id)]}"
        i += 1
    text += f"\n\nИтого: {round(total, 2)}"
    text += f"\n\nКонтакт: {phone_number}"
    text += f"\nКомментарий: \n{comment}" if comment else ""
    return text


@router.message(F.text, OrderForm.comment)
async def comment_handler(
        message: Message,
        state: FSMContext,
        user: User,
):
    if message.text == "Пропустить":
        await state.update_data(
            comment=None,
        )
    else:
        await state.update_data(
            comment=message.text,
        )

    cart_service = CartService()
    cart = await cart_service.get_cart(
        user.id
    )
    data = await state.get_data()
    text = await get_order_text(
        phone_number=data['phone_number'],
        comment=data['comment'],
        cart=cart,
    )
    await message.answer(
        text,
        reply_markup=confirm_kb(user.language)
    )
    await state.set_state(OrderForm.confirm)

@router.callback_query(F.data == "yes", OrderForm.confirm)
async def confirm_handler(
        cb: CallbackQuery,
        state: FSMContext,
        user: User,
):
    async with async_session() as session:
        manager = OrderManager(session)
        cart_service = CartService()
        cart = await cart_service.get_cart(user.id)
        data = await state.get_data()
        total = await cart_service.get_total_price(session, user.id)
        order_id = await manager.create(
            phone_number=data['phone_number'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            comment=data['comment'],
            client_id=user.id,
            products=cart,
            total_price=total,
        )
        text = await get_order_text(
            phone_number=data['phone_number'],
            comment=data['comment'],
            cart=cart,
            order_id=order_id,
        )
        await cart_service.clear_cart(user.id)
        await cb.message.answer(
            text
        )
        await state.clear()
        await cb.message.answer(
            "Выберите Действие",
            reply_markup=start_keyboard(user.language)
        )