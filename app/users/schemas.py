from pydantic import BaseModel, Field, EmailStr

class ResponseUserGet(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя, от 1 до 50 символов")
    password: str = Field(..., min_length=1, max_length=50, description="Пароль, от 1 до 50 символов")
    email: EmailStr = Field(..., description="Электронная почта")
    weight: float = Field(..., ge=0, description="Масса должна быть неотрицательной")
    LBS: float = Field(..., ge=0, description="Сухая масса должна быть неотрицательной")
    fat_percentage: float = Field(..., ge=0, le=100, description="Процент жира должен быть от 0 до 100")

class ResponseUserRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя, от 1 до 50 символов")
    password: str = Field(..., min_length=1, max_length=50, description="Пароль, от 1 до 50 символов")
    email: EmailStr = Field(..., description="Электронная почта")

class ResponseUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")

class ResponseUserMakeAdmin(BaseModel):
    id: int
    is_admin: bool = False

class ResponseUserUpdate(BaseModel):
    name: str = Field(None, min_length=1, max_length=50, description="Имя пользователя, от 1 до 50 символов")
    email: EmailStr = Field(None, description="Электронная почта")
    weight: float = Field(None, ge=0, description="Масса должна быть неотрицательной")
    LBS: float = Field(None, ge=0, description="Сухая масса должна быть неотрицательной")
    fat_percentage: float = Field(None, ge=0, le=100, description="Процент жира должен быть от 0 до 100")