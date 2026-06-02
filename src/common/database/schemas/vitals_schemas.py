from pydantic import BaseModel, Field, model_validator

###########################################################
### Модели для запросов ###
###########################################################

class RequestVitalCreate(BaseModel):
    weight: float = Field(..., ge=0, description="Масса в килограммах")
    LBS: float = Field(None, ge=0, description="Cухая масса в килограммах")
    fat_percentage: float = Field(None, ge=0, le=100, description="Процент жира")

    @model_validator(mode="after")
    def calculate_and_validate_metrics(self):
        if self.fat_percentage is None and self.LBS is not None:
            self.fat_percentage = (1 - self.LBS / self.weight) * 100
        elif self.fat_percentage is not None and self.LBS is None:
            self.LBS = self.weight * (1 - self.fat_percentage / 100)
        elif self.fat_percentage is not None and self.LBS is not None:
            expected_lbs = self.weight * (1 - self.fat_percentage / 100)
            if abs(self.LBS - expected_lbs) > 0.1:  # Сравниваем с погрешностью
                raise ValueError('Неверно введены сухая масса или процент жира. Введите что-то одно.')
        return self

###########################################################
### Модели для ответов ###
###########################################################

class ResponseVitalGet(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя, от 1 до 50 символов")
    weight: float = Field(..., ge=0, description="Масса в килограммах")
    LBS: float = Field(None, ge=0, description="Cухая масса в килограммах")
    fat_percentage: float = Field(None, ge=0, le=100, description="Процент жира")