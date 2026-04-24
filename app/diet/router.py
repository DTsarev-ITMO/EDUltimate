from fastapi import Response
from app.food.dao import FoodDAO
from app.diet.dao import DietFoodDAO, DietDAO
from app.users.schemas import ResponseUserRegister, ResponseUserAuth, ResponseUserMakeAdmin, ResponseUserUpdate, ResponseUserUpdatePassword
from app.diet.schemas import ResponseDietGet
from fastapi import APIRouter, HTTPException, status, Depends
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependencies import get_current_user, get_current_admin_user, get_current_super_admin_user
from app.users.models import User

router = APIRouter(prefix='/diet', tags=['Работа с диетой'])

@router.get("/", summary="Получить диету текущего пользователя")
async def get_diet(current_user: User = Depends(get_current_user)) -> ResponseDietGet:
    diet = await DietDAO.find_one_or_none(user_id=current_user.id)
    return diet

@router.put("/add_food/", summary="Добавить продукт в диету")
async def add_food_to_diet(food_name: str, mass, current_user: User = Depends(get_current_user)) -> dict:
    food = await FoodDAO.find_one_or_none(name=food_name)
    if not food:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Продукт не найден'
        )
    check = await DietFoodDAO.add(filter_by={'user_id': current_user.id}, food_id=food.id, mass=mass)
    if check:
        return {"message": "Диета успешно обновлена!"}
    else:
        return {"message": "Ошибка при обновлении диеты!"}

@router.delete("/delete_food/", summary="Удалить продукт из диеты")
async def delete_food_from_diet(food_name: str, current_user: User = Depends(get_current_user)):
    food = await FoodDAO.find_one_or_none(name=food_name)
    check = await DietFoodDAO.delete(user_id=current_user.id, food_id=food.id)
    if check:
        return {"message": "Диета успешно обновлена!"}
    else:
        return {"message": "Ошибка при обновлении диеты!"}