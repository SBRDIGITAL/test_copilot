# AsyncHTTPClient - Асинхронный HTTP-клиент

Модуль предоставляет удобный асинхронный HTTP-клиент на основе aiohttp с поддержкой всех основных HTTP-методов и гибкими параметрами конфигурации.

## Особенности

- ✅ Поддержка всех HTTP-методов (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
- ✅ Контекстный менеджер (`async with`)
- ✅ Гибкие параметры конфигурации
- ✅ Базовый URL и заголовки по умолчанию
- ✅ Настраиваемые таймауты
- ✅ Обработка ошибок
- ✅ Быстрые функции для одиночных запросов
- ✅ Полная документация на русском языке

## Установка

Убедитесь, что у вас установлен aiohttp:

```bash
pip install aiohttp
```

## Базовое использование

### С контекстным менеджером (рекомендуется)

```python
import asyncio
from app.modules import AsyncHTTPClient

async def main():
    async with AsyncHTTPClient() as client:
        # GET-запрос
        response = await client.get('https://httpbin.org/get')
        data = await response.json()
        print(data)
        
        # POST-запрос с JSON
        response = await client.post(
            'https://httpbin.org/post',
            json={'message': 'Привет мир!'}
        )
        data = await response.json()
        print(data)

asyncio.run(main())
```

### С базовым URL

```python
async def main():
    async with AsyncHTTPClient(
        base_url='https://api.example.com',
        headers={'Authorization': 'Bearer token123'}
    ) as client:
        
        # Все запросы будут относительно base_url
        response = await client.get('/users')
        response = await client.post('/users', json={'name': 'Иван'})
```

## Все HTTP-методы

```python
async def all_methods_example():
    async with AsyncHTTPClient(base_url='https://httpbin.org') as client:
        
        # GET с параметрами
        response = await client.get('/get', params={'param1': 'value1'})
        
        # POST с JSON
        response = await client.post('/post', json={'key': 'value'})
        
        # PUT с данными
        response = await client.put('/put', json={'update': 'data'})
        
        # PATCH
        response = await client.patch('/patch', json={'patch': 'data'})
        
        # DELETE
        response = await client.delete('/delete')
        
        # HEAD (только заголовки)
        response = await client.head('/get')
        
        # OPTIONS
        response = await client.options('/get')
```

## Быстрые функции

Для одиночных запросов можно использовать быстрые функции:

```python
from app.modules import get, post, put, delete

async def quick_requests():
    # Быстрый GET
    response = await get('https://httpbin.org/get')
    data = await response.json()
    
    # Быстрый POST
    response = await post(
        'https://httpbin.org/post',
        json={'quick': 'request'}
    )
```

## Продвинутая конфигурация

```python
import aiohttp
from app.modules import AsyncHTTPClient

async def advanced_config():
    # Кастомный коннектор
    connector = aiohttp.TCPConnector(
        limit=100,  # Максимальное количество соединений
        limit_per_host=30,  # Соединений на хост
        ttl_dns_cache=300,  # Время жизни DNS-кеша
    )
    
    async with AsyncHTTPClient(
        base_url='https://api.example.com',
        timeout=30.0,  # Таймаут 30 секунд
        headers={
            'User-Agent': 'MyApp/1.0',
            'Accept': 'application/json'
        },
        connector=connector,
        trust_env=True  # Использовать прокси из переменных окружения
    ) as client:
        
        response = await client.get('/data')
```

## Обработка ошибок

```python
import asyncio
from aiohttp import ClientError

async def error_handling():
    try:
        async with AsyncHTTPClient(timeout=5.0) as client:
            response = await client.get('https://httpbin.org/delay/10')
            
    except asyncio.TimeoutError:
        print("Превышен таймаут")
    except ClientError as e:
        print(f"Ошибка клиента: {e}")
    except Exception as e:
        print(f"Общая ошибка: {e}")
```

## Параметры конструктора AsyncHTTPClient

| Параметр | Тип | Описание |
|----------|-----|----------|
| `base_url` | `str` | Базовый URL для всех запросов |
| `timeout` | `float` | Таймаут в секундах |
| `headers` | `Dict[str, str]` | Заголовки по умолчанию |
| `connector` | `aiohttp.BaseConnector` | Кастомный коннектор |
| `trust_env` | `bool` | Использовать переменные окружения для прокси |

## Методы класса

### HTTP-методы
- `get(url, params=None, **kwargs)` - GET-запрос
- `post(url, data=None, json=None, **kwargs)` - POST-запрос  
- `put(url, data=None, json=None, **kwargs)` - PUT-запрос
- `patch(url, data=None, json=None, **kwargs)` - PATCH-запрос
- `delete(url, **kwargs)` - DELETE-запрос
- `head(url, **kwargs)` - HEAD-запрос
- `options(url, **kwargs)` - OPTIONS-запрос

### Управление сессией
- `start()` - Запуск клиента (создание сессии)
- `close()` - Закрытие клиента (освобождение ресурсов)

### Универсальный метод
- `request(method, url, **kwargs)` - Выполнение запроса с любым HTTP-методом

## Примеры использования

Полные примеры использования смотрите в файле `app/modules/examples.py`.

## Тестирование

Запустите тест для проверки работоспособности:

```bash
python test_client.py
```

## Лицензия

Этот модуль создан для использования в ваших проектах.
