"""
Примеры использования AsyncHTTPClient.

Этот файл содержит различные примеры использования HTTP-клиента
для демонстрации его возможностей.
"""

import asyncio
import json
from app.modules.aiohttp_client import AsyncHTTPClient, get, post


async def example_basic_usage():
    """Базовое использование клиента с контекстным менеджером."""
    async with AsyncHTTPClient() as client:
        # GET-запрос
        response = await client.get('https://httpbin.org/get')
        data = await response.json()
        print("GET-ответ:", data)
        
        # POST-запрос с JSON
        response = await client.post(
            'https://httpbin.org/post',
            json={'message': 'Привет мир!'}
        )
        data = await response.json()
        print("POST-ответ:", data)


async def example_with_base_url():
    """Использование клиента с базовым URL."""
    async with AsyncHTTPClient(
        base_url='https://httpbin.org',
        headers={'User-Agent': 'AsyncHTTPClient/1.0'}
    ) as client:
        
        # Запросы с относительными URL
        response = await client.get('/get')
        print("Статус:", response.status)
        
        response = await client.post('/post', json={'test': 'data'})
        print("Статус:", response.status)


async def example_all_methods():
    """Демонстрация всех HTTP-методов."""
    async with AsyncHTTPClient(base_url='https://httpbin.org') as client:
        
        # GET
        response = await client.get('/get', params={'param1': 'value1'})
        print(f"GET: {response.status}")
        
        # POST
        response = await client.post('/post', json={'key': 'value'})
        print(f"POST: {response.status}")
        
        # PUT
        response = await client.put('/put', json={'update': 'data'})
        print(f"PUT: {response.status}")
        
        # PATCH
        response = await client.patch('/patch', json={'patch': 'data'})
        print(f"PATCH: {response.status}")
        
        # DELETE
        response = await client.delete('/delete')
        print(f"DELETE: {response.status}")
        
        # HEAD
        response = await client.head('/get')
        print(f"HEAD: {response.status}")
        
        # OPTIONS
        response = await client.options('/get')
        print(f"OPTIONS: {response.status}")


async def example_error_handling():
    """Обработка ошибок при работе с клиентом."""
    try:
        async with AsyncHTTPClient(timeout=5.0) as client:
            response = await client.get('https://httpbin.org/delay/10')
            print("Успешный запрос")
    except asyncio.TimeoutError:
        print("Превышен таймаут")
    except Exception as e:
        print(f"Ошибка: {e}")


async def example_quick_functions():
    """Использование быстрых функций без создания клиента."""
    # Быстрый GET
    response = await get('https://httpbin.org/get')
    data = await response.json()
    print("Быстрый GET:", data.get('url'))
    
    # Быстрый POST
    response = await post(
        'https://httpbin.org/post',
        json={'quick': 'request'}
    )
    data = await response.json()
    print("Быстрый POST:", data.get('json'))


async def example_advanced_config():
    """Продвинутая конфигурация клиента."""
    import aiohttp
    
    # Создание кастомного коннектора
    connector = aiohttp.TCPConnector(
        limit=100,  # Максимальное количество соединений
        limit_per_host=30,  # Максимальное количество соединений на хост
        ttl_dns_cache=300,  # Время жизни DNS-кеша
        use_dns_cache=True,
    )
    
    async with AsyncHTTPClient(
        base_url='https://httpbin.org',
        timeout=30.0,
        headers={
            'User-Agent': 'CustomAgent/1.0',
            'Accept': 'application/json'
        },
        connector=connector,
        trust_env=True  # Использовать прокси из переменных окружения
    ) as client:
        
        response = await client.get('/get')
        print(f"Продвинутый запрос: {response.status}")


async def main():
    """Запуск всех примеров."""
    print("=== Базовое использование ===")
    await example_basic_usage()
    
    print("\n=== Использование с базовым URL ===")
    await example_with_base_url()
    
    print("\n=== Все HTTP-методы ===")
    await example_all_methods()
    
    print("\n=== Обработка ошибок ===")
    await example_error_handling()
    
    print("\n=== Быстрые функции ===")
    await example_quick_functions()
    
    print("\n=== Продвинутая конфигурация ===")
    await example_advanced_config()


if __name__ == '__main__':
    asyncio.run(main())
