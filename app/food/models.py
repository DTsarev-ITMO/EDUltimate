from sqlalchemy.orm import Mapped, relationship
from app.database import Base, uniq_str_an, float_def0_an
from app.diet.models import DietFood
from typing import List

class Food(Base):
    name: Mapped[uniq_str_an]
    protein: Mapped[float_def0_an]
    fats: Mapped[float_def0_an]
    carbs: Mapped[float_def0_an]
    calories: Mapped[float_def0_an]

    diet_associations: Mapped[List["DietFood"]] = relationship(back_populates="foods")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"

    def __repr__(self):
        return str(self)