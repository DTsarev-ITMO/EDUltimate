import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.common.config import BACKEND_IP, BACKEND_PORT

from src.EDUltimate_api.routers import routers

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

for rt in routers:
    app.include_router(rt)

if __name__ == "__main__":
    # uvicorn.run(app, host=BACKEND_IP, port=BACKEND_PORT)
    uvicorn.run(app, host=BACKEND_IP, port=8001)