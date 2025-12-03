from datetime import datetime

from sqlalchemy import Column, BigInteger, String, DateTime
from models.base import Base


# Создание Модельки Юзера
class User(Base):
    # Название Таблицы в БД
    __tablename__ = "users"

    # Поля Таблицы
    # id INT PRIMARY KEY
    id = Column(BigInteger, primary_key=True)
    # full_name VARCHAR(320) NOT NULL
    full_name = Column(String(320), nullable=False)
    # language VARCHAR(2) DEFAULT 'ru'
    language = Column(String(2), default="ru")
    # created_at TIMESTAMP DEFAULT NOW()
    created_at = Column(DateTime, default=datetime.now)