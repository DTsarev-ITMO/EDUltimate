from fastapi import Response
from app.users.dao import UserDAO
from app.users.schemas import ResponseUserRegister, ResponseUserAuth, ResponseUserMakeAdmin, ResponseUserUpdate
from fastapi import APIRouter, HTTPException, status, Depends
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependencies import get_current_user, get_current_admin_user, get_current_super_admin_user
from app.users.models import User

router = APIRouter(prefix='/auth', tags=['Работа с пользователями'])

@router.post("/register/")
async def register_user(user_data: ResponseUserRegister) -> dict:
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await UserDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}

@router.post("/login/")
async def auth_user(response: Response, user_data: ResponseUserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="user_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}

@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data

@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="user_access_token")
    return {'message': 'Пользователь вышел из системы'}

@router.get("/all_users/")
async def get_all_users(user_data: User = Depends(get_current_admin_user)):
    return await UserDAO.find_all()

@router.post("/make_admin/")
async def make_admin(user_to_update_id: ResponseUserMakeAdmin, myself: User = Depends(get_current_super_admin_user)):
    check = await UserDAO.update(filter_by={'id': user_to_update_id}, is_admin=True)
    new_admin = await UserDAO.find_one_or_none(id=user_to_update_id)
    if check:
        return {"message": "Запись успешно обновлена!", "Новый администратор": new_admin}
    else:
        return {"message": "Ошибка при добавлении администратора!"}

@router.put("/update/")
async def update(user_data = ResponseUserUpdate, current_user: User = Depends(get_current_user)) -> dict:
    check = await UserDAO.update(filter_by={'id': current_user.id},
                                 **user_data.model_dump(exclude_none=True))
    if check:
        return {"message": "Запись успешно обновлена!", "данные пользователя": user_data}
    else:
        return {"message": "Ошибка при обновлении записи!"}



@router.delete("/delete_me/")
async def delete_me(myself: User = Depends(get_current_user)):
    check = await UserDAO.delete(id=myself.id)
    if check:
        return {"message": f"Ваш аккаунт успешно удален!"}
    else:
        return {"message": "Ошибка при удалении аккаунта"}

@router.delete("/delete/")
async def delete_user(user_to_delete_id: int, myself: User = Depends(get_current_admin_user)):
    check = await UserDAO.delete(id=user_to_delete_id)
    if check:
        return {"message": f"Аккаунт успешно удален!"}
    else:
        return {"message": "Ошибка при удалении аккаунта"}