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

class ResponseFoodUpdate(BaseModel):
    filter_name: str = Field(..., description="Название продукта для поиска")
    name: str = Field(None, min_length=1, max_length=50, description="Новое название продукта, от 1 до 50 символов")
    protein: float = Field(None, ge=0, le=100, description="Содержание белка на 100 грамм продукта, от 0 до 100 грамм")
    fats: float = Field(None, ge=0, le=100, description="Содержание жиров на 100 грамм продукта, от 0 до 100 грамм")
    carbs: float = Field(None, ge=0, le=100, description="Содержание углеводов на 100 грамм продукта, от 0 до 100 грамм")

# class ResponseFoodUpdName(BaseModel):
#     name: str = Field(..., description="Название продукта")
#     new_name: str = Field(..., min_length=1, max_length=50, description="Новое название продукта, от 1 до 50 символов")
#
# class ResponseFoodUpdProtein(BaseModel):
#     name: str = Field(..., description="Название продукта")
#     protein: float = Field(0, ge=0, le=100, description="Новое содержание белка на 100 грамм продукта, от 0 до 100 грамм")
#
# class ResponseFoodUpdFats(BaseModel):
#     name: str = Field(..., description="Название продукта")
#     fats: float = Field(0, ge=0, le=100, description="Новое содержание жира на 100 грамм продукта, от 0 до 100 грамм")
#
# class ResponseFoodUpdCarbs(BaseModel):
#     name: str = Field(..., description="Название продукта")
#     carbs: float = Field(0, ge=0, le=100, description="Новое содержание углеводов на 100 грамм продукта, от 0 до 100 грамм")