from _datetime import datetime
from enum import Enum

from pydantic import BaseModel
class LanguageEnum(str, Enum):
    en = "en"
    uz = "uz"
    ru = "ru"
class User(BaseModel):
    id: int
    full_name: str

class UserCreate(User):
    pass

# | This "or"
class UserRead(User):
    Language : LanguageEnum
    created_at: datetime | None

class LanguageChange(BaseModel):
    Language: LanguageEnum