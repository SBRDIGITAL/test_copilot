"""
Простой тест для демонстрации работы AsyncHTTPClient.
"""

import asyncio
from app.modules import AsyncHTTPClient


async def test_client():
    """Тестирование HTTP-клиента."""
    print("Запуск теста HTTP-клиента...")
    
    try:
        async with AsyncHTTPClient(
            base_url='https://httpbin.org',
            timeout=10.0,
            headers={'User-Agent': 'TestClient/1.0'}
        ) as client:
            
            # Тест GET-запроса
            print("Выполнение GET-запроса...")
            response = await client.get('/get', params={'test': 'parameter'})
            print(f"Статус GET: {response.status}")
            
            if response.status == 200:
                data = await response.json()
                print(f"URL запроса: {data.get('url')}")
                print(f"Параметры: {data.get('args')}")
            
            # Тест POST-запроса
            print("\nВыполнение POST-запроса...")
            response = await client.post(
                '/post',
                json={
                    'message': 'Тестовое сообщение',
                    'timestamp': '2025-07-01'
                }
            )
            print(f"Статус POST: {response.status}")
            
            if response.status == 200:
                data = await response.json()
                print(f"Отправленные данные: {data.get('json')}")
            
            print("\nТест успешно завершен!")
            
    except Exception as e:
        print(f"Ошибка при выполнении теста: {e}")


if __name__ == '__main__':
    asyncio.run(test_client())
