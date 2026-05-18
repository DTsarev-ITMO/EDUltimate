"""
This module sets up the asynchronous database connection using SQLAlchemy and provides session management for FastAPI as well as internal Python usage.
"""

from typing import Generator, Annotated
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine, AsyncAttrs
from src.common.config import DB_USER, DB_PASSWORD, DB_NAME, DB_EXTERNAL_IP, DB_EXTERNAL_PORT, DB_INTERNAL_IP, DB_INTERNAL_PORT
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import uuid
from sqlalchemy.dialects.postgresql import UUID

load_dotenv()

DATABASE_EXTERNAL_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_EXTERNAL_IP}:{DB_EXTERNAL_PORT}/{DB_NAME}'
DATABASE_INTERNAL_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_INTERNAL_IP}:{DB_INTERNAL_PORT}/{DB_NAME}'

engine_external = create_async_engine(DATABASE_EXTERNAL_URL, future=True)
SessionLocal_external = async_sessionmaker(bind=engine_external, expire_on_commit=False, autocommit=False,
                                  autoflush=False, class_=AsyncSession, future=True)

engine_internal = create_async_engine(DATABASE_INTERNAL_URL, future=True)
SessionLocal_internal = async_sessionmaker(bind=engine_internal, expire_on_commit=False, autocommit=False,
                                  autoflush=False, class_=AsyncSession, future=True)

@asynccontextmanager
async def async_session_maker(external=False) -> Generator:
    """
    Provides an async database session for FastAPI routes (external) and internal Python use.

    Yields:
        AsyncSession: The database session instance.
    """
    if external:
        session: AsyncSession = SessionLocal_external()
    else:
        session: AsyncSession = SessionLocal_internal()
    try:
        yield session
    finally:
        await session.close()


# # Кастомные типы данных
# uniq_str_an = Annotated[str, mapped_column(unique=True)]
# float_def0_an = Annotated[float, mapped_column(default=0)]
# int_pk = Annotated[int, mapped_column(unique=True)]

# # Базовый класс для всех моделей
# class Base(AsyncAttrs, DeclarativeBase):
#     __abstract__ = True  # Класс абстрактный, чтобы не создавать отдельную таблицу для него
#
#     id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     created_at: Mapped[datetime] = mapped_column(server_default=func.now())
#     updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
#
#     @declared_attr.directive
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower() + 's'