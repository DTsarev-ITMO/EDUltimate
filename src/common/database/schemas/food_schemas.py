from pydantic import BaseModel, Field

###########################################################
### Модели для запросов ###
###########################################################

class RequestFoodAdd(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Название продукта, от 1 до 50 символов")
    protein: float = Field(..., ge=0, le=100, description="Содержание белка на 100 грамм продукта, от 0 до 100 грамм")
    fats: float = Field(..., ge=0, le=100, description="Содержание жиров на 100 грамм продукта, от 0 до 100 грамм")
    carbs: float = Field(..., ge=0, le=100, description="Содержание углеводов на 100 грамм продукта, от 0 до 100 грамм")
    calories: float = Field(0, ge=0, description="Содержание калорий на 100 грамм продукта, не меньше 0")

class RequestFoodUpdate(BaseModel):
    name: str = Field(None, min_length=1, max_length=50, description="Название продукта, от 1 до 50 символов")
    protein: float = Field(None, ge=0, le=100, description="Содержание белка на 100 грамм продукта, от 0 до 100 грамм")
    fats: float = Field(None, ge=0, le=100, description="Содержание жиров на 100 грамм продукта, от 0 до 100 грамм")
    carbs: float = Field(None, ge=0, le=100, description="Содержание углеводов на 100 грамм продукта, от 0 до 100 грамм")
    calories: float = Field(None, ge=0, description="Содержание калорий на 100 грамм продукта, не меньше 0")

###########################################################
### Модели для ответов ###
###########################################################

class ResponseFoodGet(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Название продукта, от 1 до 50 символов")
    protein: float = Field(..., ge=0, le=100, description="Содержание белка на 100 грамм продукта, от 0 до 100 грамм")
    fats: float = Field(..., ge=0, le=100, description="Содержание жиров на 100 грамм продукта, от 0 до 100 грамм")
    carbs: float = Field(..., ge=0, le=100, description="Содержание углеводов на 100 грамм продукта, от 0 до 100 грамм")
    calories: float = Field(0, ge=0, description="Содержание калорий на 100 грамм продукта, не меньше 0")