from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.database import Base, uniq_str_an, float_def0_an
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Float, UniqueConstraint
# from app.food.models import Food
# from app.users.models import User

# Таблица-посредник (Association Object) для добавления продуктов в диету
class DietFood(Base):
    __tablename__ = "diet_food"

    # Основные поля
    diet_id: Mapped[int] = mapped_column(ForeignKey("diets.id"), primary_key=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"), primary_key=True)

    # Дополнительные поля
    mass: Mapped[float] = mapped_column(Float, default=0.0)  # Массы продуктов

    # Односторонняя связь только в сторону продуктов
    # Продукты не знают, в какие диеты они включены
    diet: Mapped["Diet"] = relationship(back_populates="food_associations")
    food: Mapped["Food"] = relationship()

# Основной класс для диеты
# Диета связана с продуктами многие ко многим в одну сторону через DietFood
class Diet(Base):
    # Основные поля
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    # Связь M:M с продуктами
    food_associations: Mapped[List["DietFood"]] = relationship(
        back_populates="diets",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    # Связь 1:1 с пользователем
    user: Mapped["User"] = relationship(back_populates="diets")
    # Вычислительные свойства
    @property
    def total_calories(self) -> float:
        return sum((assoc.food.calories * assoc.mass / 100) for assoc in self.food_associations)

    @property
    def total_proteins(self) -> float:
        return sum((assoc.food.protein * assoc.mass / 100) for assoc in self.food_associations)

    @property
    def total_fats(self) -> float:
        return sum((assoc.food.fats * assoc.mass / 100) for assoc in self.food_associations)

    @property
    def total_carbs(self) -> float:
        return sum((assoc.food.carbs * assoc.mass / 100) for assoc in self.food_associations)
