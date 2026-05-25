import asyncio
from pydantic import BaseModel, Field, EmailStr
from edultimate_api.routers.user import external
from src.common.database.models import UserRole
from src.common.database.dao import UserDAO
from src.edultimate_api.auth import get_password_hash
from fastapi import HTTPException, status

external = True

class RequestAdminCreation(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя, от 1 до 50 символов")
    password: str = Field(..., min_length=1, max_length=50, description="Пароль, от 1 до 50 символов")
    email: EmailStr = Field(..., description="Электронная почта")
    role: UserRole

async def create_super_admin(user_data: RequestAdminCreation) -> dict:
    user = await UserDAO.find_one_or_none(external=external, name=user_data.name)
    if user:
        if user.role == UserRole.SUPER_ADMIN:
            return {'message': f'Супер админ на связи.',
                    'name': user.name}
        elif user.role == UserRole.ADMIN:
            check = await UserDAO.update(external=external, filter_by={'id': user.id}, role=UserRole.SUPER_ADMIN)
            if check:
                new_admin = await UserDAO.find_one_or_none(external=external, id= user.id)
                return {'message': f'Супер админ на связи.', 'name': new_admin.name}
            else:
                return {"message": "Ошибка при добавлении администратора!"}
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Это имя уже занято'
        )
    user_dict = user_data.model_dump()
    user_dict['password_hash'] = get_password_hash(user_dict.pop("password"))
    await UserDAO.add(external=external, **user_dict)
    new_admin = await UserDAO.find_one_or_none(external=external, name=user_data.name)
    return {'message': f'Супер админ на связи.', 'name': new_admin.name}

if __name__ == '__main__':
    response = asyncio.run(create_super_admin(user_data=RequestAdminCreation(
        name='Admin',
        password='password',
        email='admin@localhost.ru',
        role=UserRole.SUPER_ADMIN,
    )))
    print(response)