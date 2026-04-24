from pydantic import BaseModel, ConfigDict
from app.food.schemas import ResponseFoodGet
from typing import List


class ResponseDietGet(BaseModel):
    user_id: int
    foods: List[ResponseFoodGet]

    # Эти поля заполняются автоматически из @property модели SQLAlchemy
    total_calories: float
    total_proteins: float
    total_fats: float
    total_carbs: float

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj):
        # Обновляем логику маппинга, чтобы включить новые поля
        data = {
            "id": obj.user_id,
            "total_calories": obj.total_calories,
            "total_proteins": obj.total_proteins,
            "total_fats": obj.total_fats,
            "total_carbs": obj.total_carbs,
            "foods": [
                {
                    "id": assoc.food.id,
                    "name": assoc.food.name,
                    "calories": assoc.food.calories,
                    "proteins": assoc.food.proteins,
                    "fats": assoc.food.fats,
                    "carbs": assoc.food.carbs,
                    "mass": assoc.mass
                }
                for assoc in obj.food_associations
            ]
        }
        return super().model_validate(data)
