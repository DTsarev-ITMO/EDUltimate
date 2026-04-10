from fastapi import APIRouter, Depends
from app.users.dao import UserDAO
from app.users.schemas import ResponseUser
from app.users.rb import RBUser

router = APIRouter(prefix='/users', tags=['Работа с пользователями'])

@router.get("/", summary="Получить всех пользователей")
async def get_all_students(request_body: RBUser = Depends()) -> list[ResponseUser]:
    return await UserDAO.find_all(**request_body.to_dict())

@router.get("/?id={id}", summary="Получить одного пользователя по id")
async def get_user_by_id(user_id: int) -> ResponseUser | dict:
    rez = await UserDAO.find_one_or_none_by_id(user_id)
    if rez is None:
        return {'message': f'Пользователь с ID {user_id} не найден!'}
    return rez

@router.get("/?username={name}", summary="Получить одного пользователя по имени")
async def get_user_by_id(name: str) -> ResponseUser | dict:
    rez = await UserDAO.find_one_or_none_by_name(name)
    if rez is None:
        return {'message': f'Пользователь {name} не найден!'}
    return rez

@router.get("/by_filter", summary="Получить одного пользователя по фильтру")
async def get_user_by_filter(request_body: RBUser = Depends()) -> ResponseUser | dict:
    rez = await UserDAO.find_one_or_none(**request_body.to_dict())
    if rez is None:
        return {'message': f'Пользователь с указанными параметрами не найден!'}
    return rez