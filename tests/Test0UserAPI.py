import unittest
import asyncio
from app.frontend.users.httpx_commands import register_user, log_in, get_me, update_me, delete_me

class FoodAPITestCase(unittest.TestCase):
    def test_01_User_register(self):
        response = asyncio.run(register_user(name='Удали_меня', email='delme@mail.ru', password='password'))
        correct_response = {'message': 'Вы успешно зарегистрированы!'}
        self.assertEqual(response, correct_response)

    def test_02_log_in(self):
        response = asyncio.run(log_in(email='delme@mail.ru', password='password'))
        self.assertIsNotNone(response['access_token'])

    def test_03_get_me(self):
        response = asyncio.run(get_me(email='delme@mail.ru', password='password'))
        self.assertEqual(response['name'], 'Удали_меня')
        self.assertEqual(response['weight'], 0.0)
        self.assertEqual(response['LBS'], 0.0)
        self.assertEqual(response['fat_percentage'], 0)

    def test_04_update_me(self):
        response = asyncio.run(update_me(email='delme@mail.ru', password='password', weight=10.0))
        self.assertEqual(response['данные пользователя']['weight'], 10.0)
        response = asyncio.run(get_me(email='delme@mail.ru', password='password'))
        self.assertEqual(response['weight'], 10.0)

    def test_05_delete_me(self):
        response = asyncio.run(delete_me(email='delme@mail.ru', password='password'))
        correct_response = {'message': 'Ваш аккаунт успешно удален!'}
        self.assertEqual(response, correct_response)

if __name__ == '__main__':
    unittest.main()