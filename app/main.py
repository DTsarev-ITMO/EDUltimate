from fastapi import FastAPI
from app.food.models import Food
from app.users.router import router as router_user
from app.food.router import router as router_food

app = FastAPI()
@app.get("/")
def read_root():
    return {"Вас приветствует Eating Disorder Ultimate -- приложение для вашего растройства пищевого поведения."}


app.include_router(router_user)
app.include_router(router_food)

# Food
#
# @app.get("/food_name={name}", response_model=None)
# def get_food_name(name: str):
#     return 'food named ' + name

# @app.post("/add_food_name", response_model=None)
# async def add_food(food: Food):
#     # Логика добавления продукта
#     return {"message": "Продукт успешно добавлен в базу", "food": food}



# Users

# @app.get("/user_name={name}", response_model=None)
# def get_user_name(name: str):
#     return 'user named ' + name
