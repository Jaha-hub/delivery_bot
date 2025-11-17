from sqlalchemy import Integer, Column, String, DateTime, ForeignKey, Numeric, Float

from models.base import Base
from models.user import User
# У заказа
# ID
# Номер телефона клиента
# клиент
# локация (кординатs) ширина долгота
#total_price

class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(20), nullable=False)
    client_id = Column(Integer,ForeignKey('user.id',ondelete="SET NULL"), nullable=True)
    width = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    total_price = Column(Numeric(16,2), nullable=False)
    comment = Column(String(520), nullable=False)


class OrderProduct(Base):
    __tablename__ = "order_products"
    order_id = Column(Integer, ForeignKey("order.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer)
    price = Column(Numeric(16,2), nullable=False)
#У каждого заказа продуктов
# Продукт
# заказ
# кол-во
# цена