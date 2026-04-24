from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.database import Base, uniq_str_an, float_def0_an
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Float, UniqueConstraint
from app.food.models import Food

# Таблица-посредник (Association Object)
class DietFood(Base):
    __tablename__ = "diet_food"

    user_id: Mapped[int] = mapped_column(ForeignKey("diets.id"), primary_key=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"), primary_key=True)
    mass: Mapped[float] = mapped_column(Float, default=0.0)  # Массы продуктов

    # Связи для удобного доступа
    diet: Mapped["Diet"] = relationship(back_populates="food_associations")
    food: Mapped["Food"] = relationship(back_populates="diet_associations")


class Diet(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    food_associations: Mapped[List["DietFood"]] = relationship(
        back_populates="diets",
        cascade="all, delete-orphan",
        lazy="joined"
    )

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
