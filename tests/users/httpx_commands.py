import httpx
from typing import Optional


headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

async def register_user(name: str, email: str,  password: str):
    url = 'http://127.0.0.1:8000/user/register/'
    data = {
        "name": name,
        "password": password,
        "email": email
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        return response.json()

async def log_in(email: str,  password: str):
    url = 'http://127.0.0.1:8000/user/login/'
    data = {
        "email": email,
        "password": password
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        return response.json()

async def get_me(email: str,  password: str):
    url = 'http://127.0.0.1:8000/user/me/'
    login_data = {
        "email": email,
        "password": password
    }
    async with httpx.AsyncClient() as client:
        await client.post('http://127.0.0.1:8000/user/login/', headers=headers, json=login_data)
        response = await client.get(url, headers=headers)
        return response.json()


async def update_me(email: str,
                    password: str,
                    name: Optional[str] = None,
                    new_email: Optional[str] = None,
                    weight: Optional[float] = None,
                    LBS: Optional[float] = None,
                    fat_percentage: Optional[float] = None):
    url = 'http://127.0.0.1:8000/user/update/'
    login_data = {
        "email": email,
        "password": password
    }
    data = {
        "name": name,
        "email": new_email,
        "weight": weight,
        "LBS": LBS,
        "fat_percentage": fat_percentage
    }
    data = {k: v for k, v in data.items() if v is not None}

    async with httpx.AsyncClient() as client:
        await client.post('http://127.0.0.1:8000/user/login/', headers=headers, json=login_data)
        response = await client.put(url, headers=headers, json=data)
        return response.json()

async def delete_me(email: str,  password: str):
    url = 'http://127.0.0.1:8000/user/delete_me/'
    login_data = {
        "email": email,
        "password": password
    }

    async with httpx.AsyncClient() as client:
        await client.post('http://127.0.0.1:8000/user/login/', headers=headers, json=login_data)
        response = await client.delete(url)
        return response.json()