import unittest
import asyncio
from tests.food.httpx_commands import add_food, get_food_by_name, update_food, delete_food
from common.database.schemas.food_schemas import ResponseFoodAdd, ResponseFoodUpdate

class FoodAPITestCase(unittest.TestCase):
    def test_01_Food_add(self):
        response = asyncio.run(add_food(name='УдалиМеня', protein=10.0, fats=11.0, carbs=12.0, calories=200.0))
        food = ResponseFoodAdd(name='УдалиМеня', protein=10.0, fats=11.0, carbs=12.0, calories=200.0)
        correct_response = {'message': 'Продукт успешно добавлен!',
                            'продукт': food.model_dump()}
        self.assertEqual(response, correct_response)

    def test_02_Food_get(self):
        response = asyncio.run(get_food_by_name(name='УдалиМеня'))
        self.assertEqual(response['name'], 'УдалиМеня')
        self.assertEqual(response['protein'], 10.0)
        self.assertEqual(response['fats'], 11.0)
        self.assertEqual(response['carbs'], 12.0)
        self.assertEqual(response['calories'], 200.0)

    def test_03_Food_update(self):
        response = asyncio.run(update_food(filter_name='УдалиМеня', protein=0.0))
        food_upd = ResponseFoodUpdate(filter_name='УдалиМеня', protein=0.0)
        food = asyncio.run(get_food_by_name(name='УдалиМеня'))
        correct_response = {'message': 'Запись успешно обновлена!',
                            'продукт': food_upd.model_dump()}
        self.assertEqual(response, correct_response)
        self.assertEqual(food['name'], 'УдалиМеня')
        self.assertEqual(food['protein'], 0.0)
        self.assertEqual(food['fats'], 11.0)
        self.assertEqual(food['carbs'], 12.0)
        self.assertEqual(food['calories'], 200.0)

    def test_04_Food_delete(self):
        response = asyncio.run(delete_food(name='УдалиМеня'))
        correct_response = {'message': 'Продукт УдалиМеня удален!'}
        self.assertEqual(response, correct_response)

if __name__ == '__main__':
    unittest.main()