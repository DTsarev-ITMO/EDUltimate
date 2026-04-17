import requests
from bs4 import BeautifulSoup as bs

URL = "https://calorizator.ru/product/all"

def parse_calories(html):
    soup = bs(html, 'html.parser')
    products = []

    # Находим все строки таблицы
    rows = soup.find_all('tr')

    for row in rows:
        # Извлекаем данные, используя соответствующие классы
        try:
            name = row.find('td', class_='views-field-title').get_text(strip=True)
            protein = row.find('td', class_='views-field-field-protein-value').get_text(strip=True)
            fat = row.find('td', class_='views-field-field-fat-value').get_text(strip=True)
            carbs = row.find('td', class_='views-field-field-carbohydrate-value').get_text(strip=True)
            kcal = row.find('td', class_='views-field-field-kcal-value').get_text(strip=True)

            # Собираем данные в словарь
            product_data = {
                'название': name,
                'белки': float(protein) if protein else 0.0,
                'жиры': float(fat) if fat else 0.0,
                'углеводы': float(carbs) if carbs else 0.0,
                'калории': int(kcal) if kcal else 0
            }
            products.append(product_data)
        except:
            pass

    return products


if __name__ == '__main__':
    html_data = requests.get(URL)
    if html_data.status_code == 200:
        data = parse_calories(html_data.text)

        for item in data:
            print(f"Продукт: {item['название']}")
            print(f"  Б: {item['белки']} | Ж: {item['жиры']} | У: {item['углеводы']} | Ккал: {item['калории']}")
            print("-" * 30)
    else:
        print(html_data.status_code)