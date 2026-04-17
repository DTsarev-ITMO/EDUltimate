import asyncio
import aiohttp

from tests.users.httpx_commands import register_user, log_in, get_me, update_me, delete_me

if __name__ == '__main__':
    response = asyncio.run(delete_me(email='delme@mail.ru', password='password'))
    print(response, {'message': 'Ваш аккаунт успешно удален!'})