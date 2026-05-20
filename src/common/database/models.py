import enum
from sqlalchemy import Enum, text, func, ForeignKey
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

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
class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class User(Base):
    name: Mapped[uniq_str_an]
    email: Mapped[uniq_str_an]
    password_hash: Mapped[str]

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False
    )

    vital: Mapped["UserVital"] = relationship(back_populates="user", uselist=False, lazy="joined")
    diet: Mapped["Diet"] = relationship(back_populates="user", uselist=False, lazy="joined")

    extend_existing = True


class UserVital(Base):
    weight: Mapped[float_def0_an]
    LBS: Mapped[float_def0_an]
    fat_percentage: Mapped[float_def0_an]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="vital")


###########################################################
### Работа с питанием ###
###########################################################


class Food(Base):
    name: Mapped[uniq_str_an]
    protein: Mapped[float_def0_an]
    fats: Mapped[float_def0_an]
    carbs: Mapped[float_def0_an]
    calories: Mapped[float_def0_an]


class DietFood(Base):
    __tablename__ = "diet_foods"

    diet_id: Mapped[int] = mapped_column(ForeignKey("diets.id", ondelete="CASCADE"), primary_key=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id", ondelete="CASCADE"), primary_key=True)

    mass: Mapped[float]

    diet: Mapped["Diet"] = relationship(back_populates="food_associations")
    food: Mapped["Food"] = relationship()


class Diet(Base):
    total_protein: Mapped[float] = mapped_column(default=0.0)
    total_fats: Mapped[float] = mapped_column(default=0.0)
    total_carbs: Mapped[float] = mapped_column(default=0.0)
    total_calories: Mapped[float] = mapped_column(default=0.0)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    user: Mapped["User"] = relationship(back_populates="diet")

    food_associations: Mapped[list["DietFood"]] = relationship(back_populates="diet", cascade="all, delete-orphan")

    def calculate_totals(self) -> None:
        self.total_protein = 0.0
        self.total_fats = 0.0
        self.total_carbs = 0.0
        self.total_calories = 0.0

        for assoc in self.food_associations:
            multiplier = assoc.mass / 100.0
            self.total_protein += assoc.food.protein * multiplier
            self.total_fats += assoc.food.fats * multiplier
            self.total_carbs += assoc.food.carbs * multiplier
            self.total_calories += assoc.food.calories * multiplier