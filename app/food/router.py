from fastapi import APIRouter, Depends
from app.food.dao import FoodDAO
from app.food.schemas import ResponseFoodGet, ResponseFoodAdd, ResponseFoodUpdate,ResponseFoodUpdName,ResponseFoodUpdProtein, ResponseFoodUpdFats, ResponseFoodUpdCarbs
from app.food.rb import RBFood

router = APIRouter(prefix='/food', tags=['Работа с продуктами'])

@router.get("/", summary="Получить все продукты", response_model=list[ResponseFoodGet])
async def get_all_foods():
    return await FoodDAO.find_all()

@router.get("/by_filter", summary="Получить один продукт по фильтру")
async def get_student_by_filter(request_body: RBFood = Depends()) -> ResponseFoodGet | dict:
    rez = await FoodDAO.find_one_or_none(**request_body.to_dict())
    if rez is None:
        return {'message': f'Продукт с указанными параметрами не найден!'}
    return rez

@router.post("/add/")
async def add_food(food: ResponseFoodAdd) -> dict:
    check = await FoodDAO.add(**food.model_dump())
    if check:
        return {"message": "Продукт успешно добавлен!", "продукт": food}
    else:
        return {"message": "Ошибка при добавлении продукта!"}

# @router.put("/update/")
# async def update_name(food: ResponseFoodUpdate) -> dict:
#     check = await FoodDAO.update(filter_by={'food_name': food.name},
#                                    name=food.new_name)
#     if check:
#         return {"message": "Запись успешно обновлена!", "food": food}
#     else:
#         return {"message": "Ошибка при обновлении записи!"}

@router.put("/update_protein/")
async def update_protein(food: ResponseFoodUpdProtein) -> dict:
    check = await FoodDAO.update(filter_by={'name': food.name},
                                   protein=food.protein)
    if check:
        return {"message": "Содержание белка успешно обновлено!", "food": food}
    else:
        return {"message": "Ошибка при обновлении содержания белка!"}

@router.delete("/delete/{food_name}")
async def delete_food(food_name: str) -> dict:
    check = await FoodDAO.delete(name=food_name)
    if check:
        return {"message": f"Продукт {food_name} удален!"}
    else:
        return {"message": "Ошибка при удалении продукта!"}