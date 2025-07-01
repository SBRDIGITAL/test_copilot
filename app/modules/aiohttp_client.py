"""
Модуль для работы с HTTP-запросами с использованием aiohttp.

Этот модуль предоставляет асинхронный HTTP-клиент с поддержкой
всех основных HTTP-методов и гибкой конфигурацией.
"""

import asyncio
from typing import Any, Dict, Optional, Union, Mapping
import aiohttp
from aiohttp import ClientSession, ClientTimeout, ClientResponse


class AsyncHTTPClient:
    """
    Асинхронный HTTP-клиент для работы с различными HTTP-методами.
    
    Этот класс предоставляет удобный интерфейс для выполнения HTTP-запросов
    с поддержкой контекстного менеджера и гибкими параметрами настройки.
    
    Attributes:
        session: Сессия aiohttp для выполнения запросов
        base_url: Базовый URL для всех запросов
        default_headers: Заголовки по умолчанию для всех запросов
        timeout: Таймаут для запросов
    """
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[float] = 30.0,
        headers: Optional[Dict[str, str]] = None,
        connector: Optional[aiohttp.BaseConnector] = None,
        trust_env: bool = False,
        **kwargs
    ) -> None:
        """
        Инициализация HTTP-клиента.
        
        Args:
            base_url: Базовый URL для всех запросов
            timeout: Таймаут для запросов в секундах
            headers: Заголовки по умолчанию
            connector: Коннектор для сессии
            trust_env: Доверять переменным окружения для прокси
            **kwargs: Дополнительные параметры для ClientSession
        """
        self.base_url = base_url
        self.default_headers = headers or {}
        self.timeout = ClientTimeout(total=timeout) if timeout else None
        self.connector = connector
        self.trust_env = trust_env
        self.session_kwargs = kwargs
        self.session: Optional[ClientSession] = None
        self._closed = False
    
    async def __aenter__(self) -> 'AsyncHTTPClient':
        """
        Вход в контекстный менеджер.
        
        Returns:
            Экземпляр клиента с открытой сессией
        """
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Выход из контекстного менеджера.
        
        Args:
            exc_type: Тип исключения
            exc_val: Значение исключения  
            exc_tb: Трассировка исключения
        """
        await self.close()
    
    async def start(self) -> None:
        """
        Запуск клиента и создание сессии.
        
        Raises:
            RuntimeError: Если сессия уже создана
        """
        if self.session and not self.session.closed:
            raise RuntimeError("Сессия уже создана")
        
        self.session = ClientSession(
            base_url=self.base_url,
            headers=self.default_headers,
            timeout=self.timeout,
            connector=self.connector,
            trust_env=self.trust_env,
            **self.session_kwargs
        )
        self._closed = False
    
    async def close(self) -> None:
        """
        Закрытие клиента и освобождение ресурсов.
        """
        if self.session and not self.session.closed:
            await self.session.close()
        self._closed = True
    
    def _ensure_session(self) -> None:
        """
        Проверка наличия активной сессии.
        
        Raises:
            RuntimeError: Если сессия не создана или закрыта
        """
        if not self.session or self.session.closed or self._closed:
            raise RuntimeError(
                "Сессия не создана или закрыта. "
                "Используйте контекстный менеджер или вызовите start()"
            )
    
    async def request(
        self,
        method: str,
        url: str,
        params: Optional[Mapping[str, Any]] = None,
        data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        allow_redirects: bool = True,
        **kwargs
    ) -> ClientResponse:
        """
        Выполнение HTTP-запроса.
        
        Args:
            method: HTTP-метод (GET, POST, PUT, DELETE и т.д.)
            url: URL для запроса
            params: Параметры запроса
            data: Данные для отправки в теле запроса
            json: JSON-данные для отправки
            headers: Заголовки запроса
            cookies: Куки для запроса
            timeout: Таймаут для конкретного запроса
            allow_redirects: Разрешить автоматические перенаправления
            **kwargs: Дополнительные параметры для запроса
            
        Returns:
            Ответ сервера
            
        Raises:
            RuntimeError: Если сессия не создана
            aiohttp.ClientError: При ошибках выполнения запроса
        """
        self._ensure_session()
        
        # Объединение заголовков
        merged_headers = self.default_headers.copy()
        if headers:
            merged_headers.update(headers)
        
        # Установка таймаута для конкретного запроса
        request_timeout = None
        if timeout:
            request_timeout = ClientTimeout(total=timeout)
        
        return await self.session.request(
            method=method.upper(),
            url=url,
            params=params,
            data=data,
            json=json,
            headers=merged_headers,
            cookies=cookies,
            timeout=request_timeout,
            allow_redirects=allow_redirects,
            **kwargs
        )
    
    async def get(
        self,
        url: str,
        params: Optional[Mapping[str, Any]] = None,
        **kwargs
    ) -> ClientResponse:
        """
        Выполнение GET-запроса.
        
        Args:
            url: URL для запроса
            params: Параметры запроса
            **kwargs: Дополнительные параметры
            
        Returns:
            Ответ сервера
        """
        return await self.request('GET', url, params=params, **kwargs)
    
    async def post(
        self,
        url: str,
        data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> ClientResponse:
        """
        Выполнение POST-запроса.
        
        Args:
            url: URL для запроса
            data: Данные для отправки
            json: JSON-данные для отправки
            **kwargs: Дополнительные параметры
            
        Returns:
            Ответ сервера
        """
        return await self.request('POST', url, data=data, json=json, **kwargs)
    
    async def put(
        self,
        url: str,
        data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> ClientResponse:
        """
        Выполнение PUT-запроса.
        
        Args:
            url: URL для запроса
            data: Данные для отправки
            json: JSON-данные для отправки
            **kwargs: Дополнительные параметры
            
        Returns:
            Ответ сервера
        """
        return await self.request('PUT', url, data=data, json=json, **kwargs)
    
    async def patch(
        self,
        url: str,
        data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> ClientResponse:
        """
        Выполнение PATCH-запроса.
        
        Args:
            url: URL для запроса
            data: Данные для отправки
            json: JSON-данные для отправки
            **kwargs: Дополнительные параметры
            
        Returns:
            Ответ сервера
        """
        return await self.request('PATCH', url, data=data, json=json, **kwargs)
    
    async def delete(
        self,
        url: str,
        **kwargs
    ) -> ClientResponse:
        """
        Выполнение DELETE-запроса.
        
        Args:
            url: URL для запроса
            **kwargs: Дополнительные параметры
            
        Returns:
            Ответ сервера
        """
        return await self.request('DELETE', url, **kwargs)
    
    async def head(
        self,
        url: str,
        **kwargs
    ) -> ClientResponse:
        """
        Выполнение HEAD-запроса.
        
        Args:
            url: URL для запроса
            **kwargs: Дополнительные параметры
            
        Returns:
            Ответ сервера
        """
        return await self.request('HEAD', url, **kwargs)
    
    async def options(
        self,
        url: str,
        **kwargs
    ) -> ClientResponse:
        """
        Выполнение OPTIONS-запроса.
        
        Args:
            url: URL для запроса
            **kwargs: Дополнительные параметры
            
        Returns:
            Ответ сервера
        """
        return await self.request('OPTIONS', url, **kwargs)


# Вспомогательные функции для быстрого использования

async def get(url: str, **kwargs) -> ClientResponse:
    """
    Быстрый GET-запрос без создания клиента.
    
    Args:
        url: URL для запроса
        **kwargs: Параметры для запроса
        
    Returns:
        Ответ сервера
    """
    async with AsyncHTTPClient() as client:
        return await client.get(url, **kwargs)


async def post(url: str, **kwargs) -> ClientResponse:
    """
    Быстрый POST-запрос без создания клиента.
    
    Args:
        url: URL для запроса
        **kwargs: Параметры для запроса
        
    Returns:
        Ответ сервера
    """
    async with AsyncHTTPClient() as client:
        return await client.post(url, **kwargs)


async def put(url: str, **kwargs) -> ClientResponse:
    """
    Быстрый PUT-запрос без создания клиента.
    
    Args:
        url: URL для запроса
        **kwargs: Параметры для запроса
        
    Returns:
        Ответ сервера
    """
    async with AsyncHTTPClient() as client:
        return await client.put(url, **kwargs)


async def delete(url: str, **kwargs) -> ClientResponse:
    """
    Быстрый DELETE-запрос без создания клиента.
    
    Args:
        url: URL для запроса
        **kwargs: Параметры для запроса
        
    Returns:
        Ответ сервера
    """
    async with AsyncHTTPClient() as client:
        return await client.delete(url, **kwargs)
