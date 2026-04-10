import asyncio
import httpx


async def add_food(food_name: str, protein: float, fats: float, carbs: float):
    url = 'http://127.0.0.1:8000/food/add/'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "name": food_name,
        "protein": protein,
        "fats": fats,
        "carbs": carbs
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        return response.json()

# вызов функции
if __name__ == '__main__':
    # response = asyncio.run(add_food(food_name=, protein= , fats= , carbs=))
    print(response)