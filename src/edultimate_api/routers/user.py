from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends, Response, Query
from src.common.database.dao import UserDAO
from src.common.database.schemas.user_schemas import *
from src.edultimate_api.auth import get_password_hash, authenticate_user, create_access_token
from src.edultimate_api.dependencies import get_current_user, get_current_admin_user, get_current_super_admin_user
from src.common.database.models import User, UserRole


router = APIRouter(prefix='/user', tags=['Работа с пользователями'])


@router.get("/")
async def get_all_users(admin: User = Depends(get_current_admin_user)) -> list[ResponseUserGet] | None:
    return await UserDAO.find_all()


@router.get("/me/", response_model=None)
async def get_me(user_data: User = Depends(get_current_user)) -> User:
    return user_data


@router.post("/register/",
             summary="Зарегистрировать нового пользователя",
             response_model=dict,
             status_code=status.HTTP_201_CREATED
             )
async def register_user(user_data: RequestUserRegister) -> dict:
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.model_dump()
    user_dict['password_hash'] = get_password_hash(user_dict.pop("password"))
    await UserDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/")
async def auth_user(response: Response, user_data: RequestUserAuth) -> dict:
    check = await authenticate_user(
        email=user_data.email,
        password=user_data.password
    )
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="user_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


@router.post("/logout/")
async def logout_user(response: Response) -> dict:
    response.delete_cookie(key="user_access_token")
    return {'message': 'Пользователь вышел из системы'}


@router.post("/make_admin/")
async def make_admin(
        user_to_update_id: UUID,
        super_admin: User = Depends(get_current_super_admin_user),
) -> dict:
    check = await UserDAO.update(filter_by={'id': user_to_update_id}, role=UserRole.ADMIN)
    if check:
        new_admin = await UserDAO.find_one_or_none(id=user_to_update_id)
        return {"message": "Запись успешно обновлена!", "Новый администратор": new_admin}
    else:
        return {"message": "Ошибка при добавлении администратора!"}


@router.put("/update/")
async def update(
        user_data: RequestUserUpdate,
        current_user: User = Depends(get_current_user)
) -> dict:
    check = await UserDAO.update(
        filter_by={'id': current_user.id},
        **user_data.model_dump(exclude_none=True)
    )
    if check:
        return {"message": "Запись успешно обновлена!", "данные пользователя": user_data}
    else:
        return {"message": "Ошибка при обновлении записи!"}


@router.put("/update_password/")
async def update_pass(
        old_password: RequestCheckPassword,
        new_password: RequestUserUpdatePassword,
        current_user: User = Depends(get_current_user),
) -> dict:
    check = await authenticate_user(email=current_user.email, password=old_password.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверный пароль')
    if new_password.password_1 != new_password.password_2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Пароли не совпадают')
    new_password = get_password_hash(new_password.password_1)
    check = await UserDAO.update(
        filter_by={'id': current_user.id},
        password=new_password
    )
    if check:
        return {"message": "Пароль успешно изменен!"}
    else:
        return {"message": "Ошибка при изменении пароля!"}


@router.delete("/delete_me/")
async def delete_me(
        password: RequestCheckPassword,
        current_user: User = Depends(get_current_user),
) -> dict:
    check = await authenticate_user(email=current_user.email, password=password.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверный пароль')
    check = await UserDAO.delete(id=current_user.id)
    if check:
        return {"message": f"Ваш аккаунт успешно удален!"}
    else:
        return {"message": "Ошибка при удалении аккаунта"}


@router.delete("/delete/{user_id}")
async def delete_user(
        user_id: UUID,
        admin: User = Depends(get_current_super_admin_user),
) -> dict:
    check = await UserDAO.delete(id=user_id)
    if check:
        return {"message": f"Аккаунт успешно удален!"}
    else:
        return {"message": "Ошибка при удалении аккаунта"}