from fastapi import APIRouter, Depends, Query, HTTPException
from src.common.database.dao import FoodDAO
from src.common.database.schemas.food_schemas import ResponseFood
from src.common.database.schemas.base_schemas import RequestGetID
from src.edultimate_api.dependencies import get_current_admin_user
from src.common.database.models import User


router = APIRouter(prefix='/food', tags=['Работа с продуктами'])


@router.get("/", summary="Получить все продукты", response_model=list[ResponseFood])
async def get_all_foods(external: bool = Query(default=False)) -> list[ResponseFood]:
    return await FoodDAO.find_all(external=external)


@router.get("/by_filter", summary="Получить один продукт по фильтру")
async def get_food_by_filter(
        external: bool = Query(default=False),
        name: str = Query(..., min_length=1, max_length=50, description="Название продукта"),
) -> ResponseFood:
    food = await FoodDAO.find_one_or_none(external=external, name=name)
    if not food:
        raise HTTPException(status_code=404, detail="Продукт не найден!")
    return food


@router.post("/add/")
async def add_food(food: ResponseFood, external: bool = Query(default=False),
                   current_user: User = Depends(get_current_admin_user)) -> dict:
    check = await FoodDAO.add(external=external, **food.model_dump())
    if check:
        return {"message": "Продукт успешно добавлен!", "продукт": food}
    else:
        return {"message": "Ошибка при добавлении продукта!"}


@router.put("/update/")
async def update(
        request: RequestGetID,
        food: ResponseFood, external: bool = Query(default=False),
                 current_user: User = Depends(get_current_admin_user)) -> dict:
    check = await FoodDAO.update(external=external, filter_by={'id': request.id},
                                 **food.model_dump(exclude_none=True))
    if check:
        return {"message": "Запись успешно обновлена!", "продукт": food}
    else:
        return {"message": "Ошибка при обновлении записи!"}


@router.delete("/delete/{food_name}")
async def delete_food(
        request: RequestGetID,
        external: bool = Query(default=False),
        current_user: User = Depends(get_current_admin_user)) -> dict:
    check = await FoodDAO.delete(external=external, id=request.id)
    if check:
        return {"message": f"Продукт удален!"}
    else:
        return {"message": "Ошибка при удалении продукта!"}