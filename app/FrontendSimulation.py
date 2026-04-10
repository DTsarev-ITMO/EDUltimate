import asyncio
from app.Httpx import add_food, get_food_by_name, update_food, delete_food

# вызов функции
if __name__ == '__main__':
    response = asyncio.run(add_food(food_name='Куриная грудка', protein=23.6, fats=1.9, carbs=0.4))