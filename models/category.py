from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from models.base import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    photo = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)