import psycopg2
from psycopg2 import sql
from app.config import settings
import httpx
import asyncio
import requests
from bs4 import BeautifulSoup as bs

db_data = settings.get_data_for_db_external()
admin_create_data = settings.get_admin_data()
admin_data = settings.get_admin_data()
admin_data.pop("name")

url_login = 'http://127.0.0.1:8000/user/login/'
url_add_food = 'http://127.0.0.1:8000/food/add/'
URL_to_parse = 'https://calorizator.ru/product/all'
max_page = 86

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

def count_food():
    connection = psycopg2.connect(**db_data)
    cursor = connection.cursor()
    query = sql.SQL("SELECT count(*) FROM {};").format(sql.Identifier('foods'))
    cursor.execute(query)
    count = cursor.fetchone()[0]
    return count

async def add_food(data: list):
    async with httpx.AsyncClient() as client:
        # авторизация под админом
        await client.post(url_login, headers=headers, json=admin_data)
        # добавление продукта
        response = await client.post(url_add_food, headers=headers, json=data)
        return response.json()

def get_data(html):
    soup = bs(html, 'html.parser')
    products = []

    # Находим все строки таблицы
    rows = soup.find_all('tr')

    for row in rows:
        # Извлекаем данные, используя соответствующие классы
        try:
            name = row.find('td', class_='views-field-title').get_text(strip=True)
            protein = row.find('td', class_='views-field-field-protein-value').get_text(strip=True)
            fats = row.find('td', class_='views-field-field-fat-value').get_text(strip=True)
            carbs = row.find('td', class_='views-field-field-carbohydrate-value').get_text(strip=True)
            calories = row.find('td', class_='views-field-field-kcal-value').get_text(strip=True)

            # Собираем данные в словарь
            product_data = {
                'name': name,
                'protein': float(protein) if protein else 0.0,
                'fats': float(fats) if fats else 0.0,
                'carbs': float(carbs) if carbs else 0.0,
                'calories': int(calories) if calories else 0
            }

            products.append(product_data)
        except:
            pass

    return products

def parse_whole_site(URL: str, max_page: int):
    current_page = 0
    current_URL = URL
    while current_page <= max_page:
        html_data = requests.get(current_URL)
        data = get_data(html_data.text)
        for product in data:
            try:
                asyncio.run(add_food(product))
            except:
                pass
        current_page += 1
        current_URL = f'{URL}&page={current_page}'
        print(f'Спарсено {current_page} страниц из {max_page + 1}')



if __name__ == '__main__':
    # Проверим размер таблицы food
    count = count_food()
    print(f'В базе данных БЖУ продуктов {count} записей.')

    # Если записей мало, парсим с внешнего сайта
    if count < 1000:
        print(f'Парсим данные с сайта {URL_to_parse}')
        parse_whole_site(URL_to_parse, max_page)
        count = count_food()
        print(f'В базе данных БЖУ продуктов {count} записей.')