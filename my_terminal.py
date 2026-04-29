import asyncio
from fastapi import Response, Depends

from app.food.schemas import ResponseFoodAdd, ResponseFoodGet
from app.food.rb import RBFood
from app.food.router import add_food, get_food_by_filter, delete_food

from app.users.schemas import ResponseUserRegister, ResponseUserAuth, ResponseUserGet
from app.users.rb import RBUser
from app.users.router import register_user, auth_user, get_me, delete_me, get_user_by_filter

# async def get_user_by_filter(request_body: RBUser = Depends()) -> ResponseUserGet | dict:
#     user = await UserDAO.find_one_or_none(**request_body.to_dict())
#     if user is None:
#         return {'message': f'Пользователь с указанными параметрами не найден!'}
#     return user



async def main_food():
    new_food = ResponseFoodAdd(name='delme', protein=1, fats=2, carbs=3, calories=4)
    response = await add_food(new_food)
    print(response)
    filter = {'name': 'delme'}
    request_body = RBFood(**filter)
    response = await get_food_by_filter(request_body)
    print(response)
    response = await delete_food('delme')
    print(response)

async def main_user():
    user = ResponseUserRegister(name='delme2', password='password', email='delme@mail.ru')
    # response = await register_user(new_user)
    # print(response)
    # user = ResponseUserAuth(email='delme@mail.ru', password='password')
    print(user)
    request_body = RBUser(name=user.name)
    print(request_body)
    response = await get_user_by_filter(request_body)
    print(response)
    # response = Response()
    # response = await auth_user(response, user_data=user)
    # print(response)
    # response = await get_me()
    # print(response)
    # response = await delete_me()
    # print(response)

if __name__ == "__main__":
    asyncio.run(main_user())



# async def register_user(user_data: ResponseUserRegister) -> dict:
#     user = await UserDAO.find_one_or_none(email=user_data.email)
#     if user:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail='Пользователь уже существует'
#         )
#     user_dict = user_data.model_dump()
#     user_dict['password'] = get_password_hash(user_data.password)
#     await UserDAO.add(**user_dict)
#     user = await UserDAO.find_one_or_none(email=user_data.email)
#     await DietDAO.add(user_id=user.id)
#     return {'message': 'Вы успешно зарегистрированы!'}