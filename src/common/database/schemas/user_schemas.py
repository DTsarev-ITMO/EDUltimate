from pydantic import BaseModel, Field, EmailStr


class ResponseUserRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя, от 1 до 50 символов")
    password: str = Field(..., min_length=1, max_length=50, description="Пароль, от 1 до 50 символов")
    email: EmailStr = Field(..., description="Электронная почта")


class ResponseUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


class ResponseUserUpdate(BaseModel):
    name: str = Field(None, min_length=1, max_length=50, description="Имя пользователя, от 1 до 50 символов")
    email: EmailStr = Field(None, description="Электронная почта")


class ResponseCheckPassword(BaseModel):
    password: str = Field(..., min_length=1, max_length=50, description="Пароль, от 1 до 50 символов")


class ResponseUserUpdatePassword(BaseModel):
    password_1: str = Field(..., min_length=1, max_length=50, description="Пароль, от 1 до 50 символов")
    password_2: str = Field(..., min_length=1, max_length=50, description="Пароль, от 1 до 50 символов")