"""
This module sets up the asynchronous database connection using SQLAlchemy and provides session management for FastAPI as well as internal Python usage.
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from src.common.config import DB_USER, DB_PASSWORD, DB_NAME, DB_EXTERNAL_IP, DB_EXTERNAL_PORT, DB_INTERNAL_PORT
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from typing import AsyncGenerator

load_dotenv()

DATABASE_EXTERNAL_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_EXTERNAL_IP}:{DB_EXTERNAL_PORT}/{DB_NAME}'
DATABASE_INTERNAL_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@db:{DB_INTERNAL_PORT}/{DB_NAME}'

engine_external = create_async_engine(DATABASE_EXTERNAL_URL, future=True, pool_pre_ping=True)
SessionLocal_external = async_sessionmaker(bind=engine_external, expire_on_commit=False, autocommit=False,
                                  autoflush=False, class_=AsyncSession, future=True)

engine_internal = create_async_engine(DATABASE_INTERNAL_URL, future=True, pool_pre_ping=True)
SessionLocal_internal = async_sessionmaker(bind=engine_internal, expire_on_commit=False, autocommit=False,
                                  autoflush=False, class_=AsyncSession, future=True)

@asynccontextmanager
async def async_session_maker(external=False) -> AsyncGenerator[AsyncSession, None]:
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