from app.dao.base import BaseDAO
from app.diet.models import DietFood, Diet
from sqlalchemy.exc import SQLAlchemyError
from app.database import async_session_maker


class DietDAO(BaseDAO):
    model = Diet

class DietFoodDAO(BaseDAO):
    model = DietFood
