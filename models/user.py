from _datetime import datetime

from sqlalchemy import String, Integer, Column, DateTime
from models.base import Base

#Создание модельки юзера
class User(Base):
    #Название таблицы
    __tablename__ = 'user'
    #id INT PRIMARY KEY
    id = Column(Integer, primary_key=True)
    #full_name VARCHAR(320) NOT NULL
    full_name = Column(String(320), nullable=False)
    # language VARCHAR(320) Default = true
    language = Column(String(2), default="ru")
    # created_at TIMESTAMP DEFAULT NOW()
    created_at = Column(DateTime, default=datetime.now)
