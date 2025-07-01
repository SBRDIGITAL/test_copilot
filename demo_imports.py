"""
Демонстрация различных способов импорта и использования AsyncHTTPClient.
"""

import asyncio


async def example_import_from_app():
    """Импорт из основного приложения."""
    from app import AsyncHTTPClient
    
    async with AsyncHTTPClient(base_url='https://httpbin.org') as client:
        response = await client.get('/get')
        print(f"Импорт из app: статус {response.status}")


async def example_import_from_modules():
    """Импорт из модулей."""
    from app.modules import AsyncHTTPClient, get, post
    
    # Использование класса
    async with AsyncHTTPClient() as client:
        response = await client.get('https://httpbin.org/get')
        print(f"Импорт из modules: статус {response.status}")
    
    # Использование быстрых функций
    response = await get('https://httpbin.org/get')
    print(f"Быстрая функция: статус {response.status}")


async def example_direct_import():
    """Прямой импорт из модуля."""
    from app.modules.aiohttp_client import AsyncHTTPClient
    
    async with AsyncHTTPClient() as client:
        response = await client.get('https://httpbin.org/get')
        print(f"Прямой импорт: статус {response.status}")


async def main():
    """Запуск всех примеров."""
    print("=== Различные способы импорта ===\n")
    
    print("1. Импорт из основного приложения:")
    await example_import_from_app()
    
    print("\n2. Импорт из модулей:")
    await example_import_from_modules()
    
    print("\n3. Прямой импорт:")
    await example_direct_import()
    
    print("\n=== Готово! ===")


if __name__ == '__main__':
    asyncio.run(main())
