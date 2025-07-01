"""
Типы и интерфейсы для модуля aiohttp_client.

Этот файл содержит типы данных и интерфейсы для улучшения
поддержки статической типизации и автодополнения в IDE.
"""

from typing import (
    Any, 
    Dict, 
    Optional, 
    Union, 
    Mapping, 
    Protocol,
    runtime_checkable
)
from aiohttp import ClientResponse


# Типы данных для HTTP-запросов
HTTPMethod = str
URL = str
Headers = Dict[str, str]
Params = Mapping[str, Any]
JSONData = Dict[str, Any]
RequestData = Union[str, bytes, Dict[str, Any]]
Cookies = Dict[str, str]


@runtime_checkable
class AsyncHTTPClientProtocol(Protocol):
    """
    Протокол для асинхронного HTTP-клиента.
    
    Определяет интерфейс, который должен реализовывать HTTP-клиент.
    """
    
    async def __aenter__(self) -> 'AsyncHTTPClientProtocol':
        """Вход в контекстный менеджер."""
        ...
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Выход из контекстного менеджера."""
        ...
    
    async def start(self) -> None:
        """Запуск клиента."""
        ...
    
    async def close(self) -> None:
        """Закрытие клиента."""
        ...
    
    async def request(
        self,
        method: HTTPMethod,
        url: URL,
        params: Optional[Params] = None,
        data: Optional[RequestData] = None,
        json: Optional[JSONData] = None,
        headers: Optional[Headers] = None,
        cookies: Optional[Cookies] = None,
        timeout: Optional[float] = None,
        allow_redirects: bool = True,
        **kwargs: Any
    ) -> ClientResponse:
        """Выполнение HTTP-запроса."""
        ...
    
    async def get(
        self,
        url: URL,
        params: Optional[Params] = None,
        **kwargs: Any
    ) -> ClientResponse:
        """GET-запрос."""
        ...
    
    async def post(
        self,
        url: URL,
        data: Optional[RequestData] = None,
        json: Optional[JSONData] = None,
        **kwargs: Any
    ) -> ClientResponse:
        """POST-запрос."""
        ...
    
    async def put(
        self,
        url: URL,
        data: Optional[RequestData] = None,
        json: Optional[JSONData] = None,
        **kwargs: Any
    ) -> ClientResponse:
        """PUT-запрос."""
        ...
    
    async def patch(
        self,
        url: URL,
        data: Optional[RequestData] = None,
        json: Optional[JSONData] = None,
        **kwargs: Any
    ) -> ClientResponse:
        """PATCH-запрос."""
        ...
    
    async def delete(
        self,
        url: URL,
        **kwargs: Any
    ) -> ClientResponse:
        """DELETE-запрос."""
        ...
    
    async def head(
        self,
        url: URL,
        **kwargs: Any
    ) -> ClientResponse:
        """HEAD-запрос."""
        ...
    
    async def options(
        self,
        url: URL,
        **kwargs: Any
    ) -> ClientResponse:
        """OPTIONS-запрос."""
        ...


# Дополнительные типы для конфигурации
ClientConfig = Dict[str, Any]
TimeoutConfig = Union[float, int, None]
