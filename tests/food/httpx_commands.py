import httpx
from typing import Optional

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

admin_data = {
    'email': 'admin@mail.ru',
    'password': 'password'
}

async def add_food(name: str, protein: float, fats: float, carbs: float, calories: float):
    url = 'http://127.0.0.1:8000/food/add/'
    data = {
        "name": name,
        "protein": protein,
        "fats": fats,
        "carbs": carbs,
        "calories": calories
    }

    async with httpx.AsyncClient() as client:
        await client.post('http://127.0.0.1:8000/user/login/', headers=headers, json=admin_data)
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


async def update_food(filter_name: str,
                      name: Optional[str] = None,
                      protein: Optional[float] = None,
                      fats: Optional[float] = None,
                      carbs: Optional[float] = None,
                      calories: Optional[float] = None):
    url = 'http://127.0.0.1:8000/food/update/'
    data = {
        "filter_name": filter_name,
        "name": name,
        "protein": protein,
        "fats": fats,
        "carbs": carbs,
        "calories": calories
    }
    data = {k: v for k, v in data.items() if v is not None}

    async with httpx.AsyncClient() as client:
        await client.post('http://127.0.0.1:8000/user/login/', headers=headers, json=admin_data)
        response = await client.put(url, headers=headers, json=data)
        return response.json()


async def delete_food(name: str):
    url = 'http://127.0.0.1:8000/food/delete/' + name

    async with httpx.AsyncClient() as client:
        await client.post('http://127.0.0.1:8000/user/login/', headers=headers, json=admin_data)
        response = await client.delete(url)
        return response.json()