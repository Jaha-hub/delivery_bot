from sqlalchemy import Float, Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from models.base import Base
from models.product import Product

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(25), nullable=False)
    client_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    total_price = Column(Numeric(16, 2), nullable=False)
    comment = Column(String(512), nullable=True)

    products = relationship(
        "OrderProduct",
        back_populates="order",
        lazy="selectin"
    )

class OrderProduct(Base):
    __tablename__ = "order_products"
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer)

    product = relationship(
        Product,
        back_populates="order_products",
        lazy="selectin",
    )

    order = relationship(
        "Order",
        back_populates="products",
        lazy="selectin",
    )

# у Заказа
# ID
# Номер Телефона Клиент
# Клиент
# ширина
# долгота
# total_price
# Комментарий

# У каждого Заказа Продуктов
# Продукт
# заказ
# Кол-во
# цена
