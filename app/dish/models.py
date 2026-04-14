# from sqlalchemy.orm import Mapped
# from app.database import , uniq_str_an, float_def0_an
from app.food.models import Food

class Dish(Food):
    # name: Mapped[uniq_str_an]
    # protein: Mapped[float_def0_an]
    # fats: Mapped[float_def0_an]
    # carbs: Mapped[float_def0_an]
    ingredients: list[Food]
    description: str

    # def __str__(self):
    #     return f"{self.__class__.__name__}(id={self.id}, name={self.name})"
    #
    # def __repr__(self):
    #     return str(self)