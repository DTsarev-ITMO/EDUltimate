from app.dao.base import BaseDAO
from app.food.models import Food


class FoodDAO(BaseDAO):
    model = Food