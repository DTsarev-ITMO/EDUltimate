from pydantic import BaseModel, Field, EmailStr


class ResponseUser(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя, от 1 до 50 символов")
    password: str = Field(..., min_length=1, max_length=50, description="Пароль пользователя, от 1 до 50 символов")
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    weight: float = Field(..., ge=0, description="Масса должна быть неотрицательной")
    LBS: float = Field(..., ge=0, description="Сухая масса должна быть неотрицательной")
    fat_percentage: float = Field(..., ge=0, le=100, description="Процент жира должен быть от 0 до 100")