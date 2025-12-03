from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class LanguageEnum(str, Enum):
    en = "en"
    uz = "uz"
    ru = "ru"


class UserBase(BaseModel):
    id: int
    full_name: str


class UserCreate(UserBase):
    pass


# | или

class UserRead(UserBase):
    language: LanguageEnum
    created_at: datetime | None


class LanguageChange(BaseModel):
    language: LanguageEnum
