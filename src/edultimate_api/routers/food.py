from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException, status
from src.common.database.dao import FoodDAO
from src.common.database.schemas.food_schemas import RequestFoodAdd, ResponseFoodGet
from src.edultimate_api.dependencies import get_current_admin_user
from src.common.database.models import User


router = APIRouter(prefix='/food', tags=['Работа с продуктами'])


@router.get("/", summary="Получить все продукты")
async def get_all_foods() -> list[ResponseFoodGet]:
    return await FoodDAO.find_all()


@router.get("/by_filter", summary="Получить один продукт по фильтру")
async def get_food_by_filter(name: str = Query(..., min_length=1, max_length=50, description="Название продукта")
                             ) -> ResponseFoodGet:
    food = await FoodDAO.find_one_or_none(name=name)
    if not food:
        raise HTTPException(status_code=404, detail="Продукт не найден!")
    return food


@router.post("/add/")
async def add_food(
        food: RequestFoodAdd,
        admin: User = Depends(get_current_admin_user)
) -> dict:
    check = await FoodDAO.add(**food.model_dump())
    if check:
        return {"message": "Продукт успешно добавлен!", "продукт": food}
    else:
        return {"message": "Ошибка при добавлении продукта!"}


@router.put("/update/{food_id}")
async def update_food(
        food_id: UUID,
        food: RequestFoodAdd,
        admin: User = Depends(get_current_admin_user)
) -> dict:
    check = await FoodDAO.update(filter_by={'id': food_id}, **food.model_dump(exclude_none=True))
    if check:
        return {"message": "Запись успешно обновлена!", "продукт": food}
    else:
        return {"message": "Ошибка при обновлении записи!"}


@router.delete("/delete/{food_id}")
async def delete_food(
        food_id: UUID,
        admin: User = Depends(get_current_admin_user)) -> dict:
    check = await FoodDAO.delete(id=food_id)
    if check:
        return {"message": f"Продукт удален!"}
    else:
        return {"message": "Ошибка при удалении продукта!"}