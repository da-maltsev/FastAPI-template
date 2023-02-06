from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import settings

engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), pool_pre_ping=True, echo=settings.IS_LOCAL
)
sync_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI_ASYNC, echo=settings.IS_LOCAL, future=True
)
async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session
