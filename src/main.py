import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.users.router import router as router_user
from src.food.router import router as router_food

app = FastAPI()

# Разрешаем фронтенду доступ
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "null"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # Важно для Cookies!
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"Вас приветствует Eating Disorder Ultimate -- приложение для вашего расстройства пищевого поведения."}

app.include_router(router_user)
app.include_router(router_food)