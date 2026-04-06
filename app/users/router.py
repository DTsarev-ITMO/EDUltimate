from fastapi import APIRouter
from app.users.dao import UserDAO
from app.users.schemas import ResponseUser

router = APIRouter(prefix='/users', tags=['Работа с пользователями'])

@router.get("/", summary="Получить всех пользователей", response_model=list[ResponseUser])
async def get_all_users():
    return await UserDAO.find_all()