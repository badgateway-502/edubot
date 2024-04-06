from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncAttrs,
)
from sqlalchemy.orm import DeclarativeBase

from .config import get_settings


_settings = get_settings()

DATABASE_URL = _settings.database_url

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine)


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    ...
