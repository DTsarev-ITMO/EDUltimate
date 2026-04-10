import asyncio
import httpx

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

async def add_food(food_name: str, protein: float, fats: float, carbs: float):
    url = 'http://127.0.0.1:8000/food/add/'
    data = {
        "name": food_name,
        "protein": protein,
        "fats": fats,
        "carbs": carbs
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        return response.json()

async def get_food_by_name(name: str):
    url = 'http://127.0.0.1:8000/food/by_filter'
    data = {
        "name": name
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=data)
        return response.json()

async def update_food_protein(name: str, protein: float):
    url = 'http://127.0.0.1:8000/food/update_protein/'
    data = {
        "name": name,
        "protein": protein
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=headers, json=data)
        return response.json()

async def delete_food(food_name: str):
    url = 'http://127.0.0.1:8000/food/delete/' + food_name

    async with httpx.AsyncClient() as client:
        response = await client.delete(url)
        return response.json()


# вызов функции
if __name__ == '__main__':
    # response = asyncio.run(add_food(food_name='УдалиМеня', protein=10.0, fats=11.0, carbs=12.0))
    response = asyncio.run(get_food_by_name(name='УдалиМеня'))
    # response = asyncio.run(update_food_protein(name='УдалиМеня', protein=0))
    # response = asyncio.run(delete_food(food_name='УдалиМеня'))
    # response = asyncio.run(add_food(food_name='Куриная грудка', protein=23.6, fats=1.9, carbs=0.4))
    # response = asyncio.run(delete_food(food_name='Куриная грудка'))
    print(response)

    # try:
    #     food=ResponseFoodUpdProtein(name='УдалиМеня', protein=0)
    #     print(food.name)  # Доступ к данным
    #     print(food.model_dump())  # Преобразование в словарь [10]
    # except ValidationError as e:
    #     print(e)