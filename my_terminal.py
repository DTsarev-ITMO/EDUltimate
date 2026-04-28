from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings
from app.database import Base
from app.users.models import User, UserData, UserStatus
from app.users.auth import get_password_hash, verify_password
from app.diet.models import Diet
from app.food.models import Food
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import asyncio

DATABASE_URL = settings.get_db_url_external()
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession)

async def create_user(name: str, email: str, password: str):
    async with AsyncSessionLocal() as session:
        async with session.begin(): # Начнет транзакцию и сам сделает commit в конце
            new_user = User(
                name=name,
                email=email,
                password=get_password_hash(password=password),
                diet=Diet(),
                userData=UserData(),
                userStatus=UserStatus()
            )
            session.add(new_user)
            try:
                await session.commit()
                print("Успех!")
            except Exception as e:
                print(e)



if __name__ == "__main__":
    asyncio.run(create_user(name="admin", email="admin@mail.ru", password="password"))
    # print(DATABASE_URL)
