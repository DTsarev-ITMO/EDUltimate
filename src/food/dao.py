from src.dao.base import BaseDAO
from src.food.models import Food


class FoodDAO(BaseDAO):
    model = Food