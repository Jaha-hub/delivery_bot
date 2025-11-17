from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from models.base import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)