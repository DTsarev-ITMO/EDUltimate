from fastapi import APIRouter, Depends, Query
from src.common.database.dao import FoodDAO
from src.common.database.schemas.food_schemas import *
from src.common.database.rb import RBFood
from src.edultimate_api.dependencies import get_current_admin_user
from src.common.database.models import User


router = APIRouter(prefix='/food', tags=['Работа с продуктами'])


@router.get("/", summary="Получить все продукты", response_model=list[ResponseFoodGet])
async def get_all_foods(external: bool = Query(default=False)) -> list[ResponseFoodGet]:
    return await FoodDAO.find_all(external=external)


@router.get("/by_filter", summary="Получить один продукт по фильтру")
async def get_food_by_filter(external: bool = Query(default=False),
                             request_body: RBFood = Depends()) -> ResponseFoodGet | dict:
    rez = await FoodDAO.find_one_or_none(external=external, **request_body.to_dict())
    if rez is None:
        return {'message': f'Продукт с указанными параметрами не найден!'}
    return rez


@router.post("/add/")
async def add_food(food: ResponseFoodAdd, external: bool = Query(default=False),
                   current_user: User = Depends(get_current_admin_user)) -> dict:
    check = await FoodDAO.add(external=external, **food.model_dump())
    if check:
        return {"message": "Продукт успешно добавлен!", "продукт": food}
    else:
        return {"message": "Ошибка при добавлении продукта!"}


@router.put("/update/")
async def update(food: ResponseFoodUpdate, external: bool = Query(default=False),
                 current_user: User = Depends(get_current_admin_user)) -> dict:
    check = await FoodDAO.update(external=external, filter_by={'name': food.filter_name},
                                 **food.model_dump(exclude={'filter_name'}, exclude_none=True))
    if check:
        return {"message": "Запись успешно обновлена!", "продукт": food}
    else:
        return {"message": "Ошибка при обновлении записи!"}


@router.delete("/delete/{food_name}")
async def delete_food(food_name: str, external: bool = Query(default=False),
                      current_user: User = Depends(get_current_admin_user)) -> dict:
    check = await FoodDAO.delete(external=external, name=food_name)
    if check:
        return {"message": f"Продукт {food_name} удален!"}
    else:
        return {"message": "Ошибка при удалении продукта!"}