from datetime import datetime
import uuid
from pydantic import BaseModel, Field, EmailStr, model_validator
from src.common.database.models import UserRole

###########################################################
### Модели для запросов ###
###########################################################

class RequestUserRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя, от 1 до 50 символов")
    password: str = Field(..., min_length=1, max_length=50, description="Пароль, от 1 до 50 символов")
    email: EmailStr = Field(..., description="Электронная почта")


class RequestUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


class RequestUserUpdate(BaseModel):
    name: str = Field(None, min_length=1, max_length=50, description="Имя пользователя, от 1 до 50 символов")
    email: EmailStr = Field(None, description="Электронная почта")


class RequestCheckPassword(BaseModel):
    password: str = Field(..., min_length=1, max_length=50, description="Пароль, от 1 до 50 символов")


class RequestUserUpdatePassword(BaseModel):
    password_1: str = Field(..., min_length=1, max_length=50, description="Пароль, от 1 до 50 символов")
    password_2: str = Field(..., min_length=1, max_length=50, description="Пароль, от 1 до 50 символов")

###########################################################
### Модели для ответов ###
###########################################################

class ResponseUserGet(BaseModel):
    id: uuid.UUID
    name: str = Field(None, min_length=1, max_length=50, description="Имя пользователя")
    role: UserRole
    email: EmailStr = Field(None, description="Электронная почта")
    created_at: datetime