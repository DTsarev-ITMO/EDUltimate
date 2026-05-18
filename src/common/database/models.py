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

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text
# from src.common.database.database import Base, uniq_str_an, float_def0_an


# Кастомные типы данных
uniq_str_an = Annotated[str, mapped_column(unique=True)]
float_def0_an = Annotated[float, mapped_column(default=0)]
int_pk = Annotated[int, mapped_column(unique=True)]


# Базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'


###########################################################
### Работа с пользователями ###
###########################################################


class User(Base):
    name: Mapped[uniq_str_an]
    email: Mapped[uniq_str_an]
    password: Mapped[str]
    weight: Mapped[float_def0_an]
    LBS: Mapped[float_def0_an]
    fat_percentage: Mapped[float_def0_an]

    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


###########################################################
### Работа с питанием ###
###########################################################


class Food(Base):
    name: Mapped[uniq_str_an]
    protein: Mapped[float_def0_an]
    fats: Mapped[float_def0_an]
    carbs: Mapped[float_def0_an]
    calories: Mapped[float_def0_an]

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"

    def __repr__(self):
        return str(self)