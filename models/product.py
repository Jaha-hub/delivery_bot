from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=False)
    price = Column(Numeric(16, 2), nullable=False)
    photo = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))

    order_products = relationship(
        "OrderProduct",
        back_populates="product",
        lazy="selectin"
    )
