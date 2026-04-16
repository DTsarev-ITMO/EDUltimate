from fastapi import FastAPI
from app.users.router import router as router_user
from app.food.router import router as router_food
# from app.pages.router import router as router_pages
# from fastapi.templating import Jinja2Templates

app = FastAPI()
# templates = Jinja2Templates(directory='app/templates')


# @app.get('/')
# async def get_root_html(request: Request):
#     return templates.TemplateResponse(request=request, name='index.html')

# origins = [
#     "http://127.0.0.1:5500",
#     "http://localhost:5500",
#     "http://127.0.0.1:8000", # Если фронтенд и бэкенд на одном порту
#     "null",                  # Важно, если вы просто открываете файл index.html двойным кликом
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True, # Обязательно True для работы с Cookies
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
@app.get("/")
def read_root():
    return {"Вас приветствует Eating Disorder Ultimate -- приложение для вашего расстройства пищевого поведения."}

app.include_router(router_user)
app.include_router(router_food)
# app.include_router(router_pages)

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
