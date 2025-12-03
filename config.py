import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from dotenv import load_dotenv
# asyncpg
engine = create_async_engine("postgresql+asyncpg://postgres:1234@localhost:5432/DeliveryBot", echo=False)

async_session = async_sessionmaker(engine, expire_on_commit=False)

load_dotenv()

TOKEN = os.getenv("TOKEN")