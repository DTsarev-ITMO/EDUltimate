from fastapi import APIRouter, Depends
from app.users.dao import UserDAO
from app.users.schemas import ResponseUser
from app.users.rb import RBUser

router = APIRouter(prefix='/users', tags=['Работа с пользователями'])

@router.get("/", summary="Получить всех пользователей", response_model=list[ResponseUser])
async def get_all_users():
    return await UserDAO.find_all()

@router.get("/by_filter", summary="Получить одного пользователя по фильтру")
async def get_user_by_filter(request_body: RBUser = Depends()) -> ResponseUser | dict:
    rez = await UserDAO.find_one_or_none(**request_body.to_dict())
    if rez is None:
        return {'message': f'Пользователь с указанными параметрами не найден!'}
    return rez