import psycopg2
from app.config import settings
import httpx
import asyncio

db_data = settings.get_data_for_db_external()
admin_create_data = settings.get_admin_data()
admin_data = settings.get_admin_data()
admin_data.pop("name")

url_add_user = 'http://127.0.0.1:8000/user/register/'
url_login = 'http://127.0.0.1:8000/user/login/'

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

async def create_admin():
    async with httpx.AsyncClient() as client:
        response = await client.post(url_add_user, headers=headers, json=admin_create_data)
        return response

def make_admin(name: str = admin_create_data['name']):
    connection = psycopg2.connect(**db_data)
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET is_admin = true WHERE name = %s", (name, ))
    cursor.execute("UPDATE users SET is_super_admin = true WHERE name = %s", (name, ))
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    # создадим админа
    response = asyncio.run(create_admin())
    # # выдадим админу все права
    make_admin()