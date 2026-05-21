from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from src.common.config import get_auth_data
from src.common.database.dao import UserDAO
from pydantic import EmailStr
from src.common.database.models import User
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


async def authenticate_user(email: EmailStr, password: str, external: bool = False) -> User:
    user = await UserDAO.find_one_or_none(external, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    if not verify_password(password=password, password_hash=user.password_hash):
        raise HTTPException(status_code=403, detail='Неверный пароль!')
    return user