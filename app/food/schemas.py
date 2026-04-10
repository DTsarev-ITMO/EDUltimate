from pydantic import BaseModel, Field, EmailStr


class ResponseFoodGet(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., min_length=1, max_length=50, description="Название продукта, от 1 до 50 символов")
    protein: float = Field(..., ge=0, le=100, description="Содержание белка на 100 грамм продукта, от 0 до 100 грамм")
    fats: float = Field(..., ge=0, le=100, description="Содержание жиров на 100 грамм продукта, от 0 до 100 грамм")
    carbs: float = Field(..., ge=0, le=100, description="Содержание углеводов на 100 грамм продукта, от 0 до 100 грамм")

class ResponseFoodAdd(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Название продукта, от 1 до 50 символов")
    protein: float = Field(0, ge=0, le=100, description="Содержание белка на 100 грамм продукта, от 0 до 100 грамм")
    fats: float = Field(0, ge=0, le=100, description="Содержание жиров на 100 грамм продукта, от 0 до 100 грамм")
    carbs: float = Field(0, ge=0, le=100, description="Содержание углеводов на 100 грамм продукта, от 0 до 100 грамм")