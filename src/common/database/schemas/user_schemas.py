from datetime import datetime
import uuid
from pydantic import BaseModel, Field, EmailStr
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


class RequestUserVitalCreate(BaseModel):
    weight: float = Field(..., ge=0, description="Масса в килограммах")
    LBS: float = Field(None, ge=0, description="Cухая масса в килограммах")
    fat_percentage: float = Field(None, ge=0, le=100, description="Процент жира")

###########################################################
### Модели для ответов ###
###########################################################

class ResponseUserGet(BaseModel):
    id: uuid.UUID
    name: str = Field(None, min_length=1, max_length=50, description="Имя пользователя")
    role: UserRole
    email: EmailStr = Field(None, description="Электронная почта")
    created_at: datetime


class ResponseUserVitalGet(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя, от 1 до 50 символов")
    weight: float = Field(..., ge=0, description="Масса в килограммах")
    LBS: float = Field(None, ge=0, description="Cухая масса в килограммах")
    fat_percentage: float = Field(None, ge=0, le=100, description="Процент жира")