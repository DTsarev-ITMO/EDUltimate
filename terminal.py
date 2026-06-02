import asyncio
from src.edultimate_api.routers.user import register_user, auth_user
from src.common.database.schemas.user_schemas import RequestUserRegister, RequestUserAuth
from fastapi import Response
from src.edultimate_api.auth import authenticate_user
from src.common.database.models import User, UserRole

user = User(email="user@user.ru", password_hash="password_hash", role=UserRole.USER)
admin = User(email="admin@admin.ru", password_hash="password_hash", role=UserRole.ADMIN)
superadmin = User(email="superadmin@admin.ru", password_hash="password_hash", role=UserRole.SUPER_ADMIN)

if __name__ == "__main__":
    # ans = asyncio.run(
    #     register_user(external=True, user_data=RequestUserRegister(name="admin", email="admin@admin.ru", password="password"))
    # )
    ans = asyncio.run(
        auth_user(external=True, response=Response(), user_data=RequestUserAuth(email="admin@admin.ru", password="password"))
    )
    # ans = asyncio.run(
    #     get_me(user_data=user)
    # )
    # ans = asyncio.run(
    #     get_all_users(user_data=admin)
    # )
    print(ans)