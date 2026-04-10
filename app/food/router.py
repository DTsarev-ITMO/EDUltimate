from fastapi import APIRouter, Depends
from app.food.dao import FoodDAO
from app.food.schemas import ResponseFoodGet, ResponseFoodAdd
from app.food.rb import RBFood

router = APIRouter(prefix='/food', tags=['Работа с продуктами'])

@router.get("/", summary="Получить все продукты", response_model=list[ResponseFoodGet])
async def get_all_foods():
    return await FoodDAO.find_all()

@router.get("/by_filter", summary="Получить один продукт по фильтру")
async def get_food_by_filter(request_body: RBFood = Depends()) -> ResponseFoodGet | dict:
    rez = await FoodDAO.find_one_or_none(**request_body.to_dict())
    if rez is None:
        return {'message': f'Пользователь с указанными параметрами не найден!'}
    return rez

@router.post("/add/")
async def add_food(food: ResponseFoodAdd) -> dict:
    check = await FoodDAO.add(**food.model_dump())
    if check:
        return {"message": "Продукт успешно добавлен!", "продукт": food}
    else:
        return {"message": "Ошибка при добавлении продукта!"}