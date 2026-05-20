import asyncio
from src.edultimate_api.routers.user import *

user_data = ResponseUserRegister(
    name="admin",
    email="admin@admin.ru",
    password_hash="password"
)

if __name__ == "__main__":
    asyncio.run(register_user(external=True, user_data=user_data))