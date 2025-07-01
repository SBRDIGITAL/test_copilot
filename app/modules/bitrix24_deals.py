"""
Модуль для работы с API Bitrix24 - операции со сделками.

Этот модуль предоставляет удобный интерфейс для выполнения CRUD операций
над сделками в Bitrix24 с использованием REST API.
"""

import asyncio
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from app.modules.aiohttp_client import AsyncHTTPClient


class Bitrix24Deal:
    """
    Класс для представления сделки Bitrix24.
    
    Attributes:
        id: ID сделки
        title: Название сделки
        stage_id: ID стадии сделки
        opportunity: Сумма сделки
        currency_id: Валюта сделки
        contact_id: ID контакта
        company_id: ID компании
        assigned_by_id: ID ответственного
        created_by_id: ID создателя
        date_create: Дата создания
        date_modify: Дата изменения
        opened: Открыта ли сделка
        closed: Закрыта ли сделка
        comments: Комментарии
        additional_info: Дополнительная информация
    """
    
    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Инициализация объекта сделки.
        
        Args:
            data: Данные сделки из API Bitrix24
        """
        self.id = data.get('ID')
        self.title = data.get('TITLE', '')
        self.stage_id = data.get('STAGE_ID', '')
        self.opportunity = float(data.get('OPPORTUNITY', 0))
        self.currency_id = data.get('CURRENCY_ID', 'RUB')
        self.contact_id = data.get('CONTACT_ID')
        self.company_id = data.get('COMPANY_ID')
        self.assigned_by_id = data.get('ASSIGNED_BY_ID')
        self.created_by_id = data.get('CREATED_BY_ID')
        self.date_create = data.get('DATE_CREATE')
        self.date_modify = data.get('DATE_MODIFY')
        self.opened = data.get('OPENED') == 'Y'
        self.closed = data.get('CLOSED') == 'Y'
        self.comments = data.get('COMMENTS', '')
        self.additional_info = data.get('ADDITIONAL_INFO', '')
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование объекта сделки в словарь.
        
        Returns:
            Словарь с данными сделки
        """
        return {
            'ID': self.id,
            'TITLE': self.title,
            'STAGE_ID': self.stage_id,
            'OPPORTUNITY': self.opportunity,
            'CURRENCY_ID': self.currency_id,
            'CONTACT_ID': self.contact_id,
            'COMPANY_ID': self.company_id,
            'ASSIGNED_BY_ID': self.assigned_by_id,
            'CREATED_BY_ID': self.created_by_id,
            'DATE_CREATE': self.date_create,
            'DATE_MODIFY': self.date_modify,
            'OPENED': 'Y' if self.opened else 'N',
            'CLOSED': 'Y' if self.closed else 'N',
            'COMMENTS': self.comments,
            'ADDITIONAL_INFO': self.additional_info
        }
    
    def __str__(self) -> str:
        """Строковое представление сделки."""
        return f"Deal(ID={self.id}, title='{self.title}', opportunity={self.opportunity})"
    
    def __repr__(self) -> str:
        """Представление сделки для отладки."""
        return f"Bitrix24Deal(id={self.id}, title='{self.title}')"


class Bitrix24DealsAPI:
    """
    API для работы со сделками в Bitrix24.
    
    Предоставляет методы для выполнения CRUD операций над сделками
    с использованием REST API Bitrix24.
    
    Attributes:
        webhook_url: URL webhook для API Bitrix24
        client: HTTP-клиент для выполнения запросов
        user_id: ID пользователя для операций
    """
    
    def __init__(
        self,
        webhook_url: str,
        user_id: Optional[int] = None,
        timeout: float = 30.0
    ) -> None:
        """
        Инициализация API клиента для Bitrix24.
        
        Args:
            webhook_url: URL webhook Bitrix24 (например: https://xxx.bitrix24.ru/rest/1/xxxxxx/)
            user_id: ID пользователя по умолчанию для операций
            timeout: Таймаут для запросов
        """
        self.webhook_url = webhook_url.rstrip('/')
        self.user_id = user_id
        self.client = AsyncHTTPClient(
            base_url=self.webhook_url,
            timeout=timeout,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
    
    async def __aenter__(self) -> 'Bitrix24DealsAPI':
        """
        Вход в контекстный менеджер.
        
        Returns:
            Экземпляр API клиента
        """
        await self.client.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Выход из контекстного менеджера.
        
        Args:
            exc_type: Тип исключения
            exc_val: Значение исключения
            exc_tb: Трассировка исключения
        """
        await self.client.close()
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Выполнение запроса к API Bitrix24.
        
        Args:
            method: HTTP метод
            endpoint: Конечная точка API
            data: Данные для отправки
            
        Returns:
            Ответ от API
            
        Raises:
            Exception: При ошибке API или сети
        """
        url = f"/{endpoint}"
        
        try:
            response = await self.client.request(
                method=method,
                url=url,
                json=data if data else None
            )
            
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"Ошибка API Bitrix24: {response.status} - {error_text}")
            
            result = await response.json()
            
            # Проверка на ошибки в ответе Bitrix24
            if 'error' in result:
                error_msg = result.get('error_description', result.get('error', 'Неизвестная ошибка'))
                raise Exception(f"Ошибка Bitrix24 API: {error_msg}")
            
            return result
            
        except Exception as e:
            raise Exception(f"Ошибка при запросе к Bitrix24: {str(e)}")
    
    async def create_deal(self, deal_data: Dict[str, Any]) -> Bitrix24Deal:
        """
        Создание новой сделки.
        
        Args:
            deal_data: Данные для создания сделки
            
        Returns:
            Созданная сделка
            
        Raises:
            Exception: При ошибке создания сделки
        """
        # Добавляем пользователя по умолчанию, если не указан
        if self.user_id and 'ASSIGNED_BY_ID' not in deal_data:
            deal_data['ASSIGNED_BY_ID'] = self.user_id
        
        request_data = {'fields': deal_data}
        
        result = await self._make_request('POST', 'crm.deal.add', request_data)
        
        deal_id = result.get('result')
        if not deal_id:
            raise Exception("Не удалось получить ID созданной сделки")
        
        # Получаем созданную сделку для возврата полного объекта
        return await self.get_deal(deal_id)
    
    async def get_deal(self, deal_id: Union[int, str]) -> Optional[Bitrix24Deal]:
        """
        Получение сделки по ID.
        
        Args:
            deal_id: ID сделки
            
        Returns:
            Объект сделки или None, если не найдена
            
        Raises:
            Exception: При ошибке получения сделки
        """
        request_data = {'id': str(deal_id)}
        
        try:
            result = await self._make_request('POST', 'crm.deal.get', request_data)
            
            deal_data = result.get('result')
            if not deal_data:
                return None
            
            return Bitrix24Deal(deal_data)
            
        except Exception as e:
            if "не найден" in str(e).lower() or "not found" in str(e).lower():
                return None
            raise
    
    async def update_deal(
        self,
        deal_id: Union[int, str],
        deal_data: Dict[str, Any]
    ) -> Bitrix24Deal:
        """
        Обновление существующей сделки.
        
        Args:
            deal_id: ID сделки для обновления
            deal_data: Новые данные сделки
            
        Returns:
            Обновленная сделка
            
        Raises:
            Exception: При ошибке обновления сделки
        """
        request_data = {
            'id': str(deal_id),
            'fields': deal_data
        }
        
        result = await self._make_request('POST', 'crm.deal.update', request_data)
        
        # Проверяем успешность обновления
        if not result.get('result'):
            raise Exception("Не удалось обновить сделку")
        
        # Возвращаем обновленную сделку
        return await self.get_deal(deal_id)
    
    async def delete_deal(self, deal_id: Union[int, str]) -> bool:
        """
        Удаление сделки по ID.
        
        Args:
            deal_id: ID сделки для удаления
            
        Returns:
            True, если сделка успешно удалена
            
        Raises:
            Exception: При ошибке удаления сделки
        """
        request_data = {'id': str(deal_id)}
        
        result = await self._make_request('POST', 'crm.deal.delete', request_data)
        
        return bool(result.get('result'))
    
    async def list_deals(
        self,
        filter_params: Optional[Dict[str, Any]] = None,
        select_fields: Optional[List[str]] = None,
        order: Optional[Dict[str, str]] = None,
        start: int = 0,
        limit: int = 50
    ) -> List[Bitrix24Deal]:
        """
        Получение списка сделок с фильтрацией.
        
        Args:
            filter_params: Параметры фильтрации (например: {'STAGE_ID': 'NEW'})
            select_fields: Поля для выборки (если не указано, выбираются все)
            order: Сортировка (например: {'DATE_CREATE': 'DESC'})
            start: Начальная позиция для пагинации
            limit: Количество записей для возврата (максимум 50)
            
        Returns:
            Список сделок
            
        Raises:
            Exception: При ошибке получения списка сделок
        """
        request_data = {
            'start': start,
            'limit': min(limit, 50)  # Bitrix24 ограничивает до 50 записей
        }
        
        if filter_params:
            request_data['filter'] = filter_params
        
        if select_fields:
            request_data['select'] = select_fields
        
        if order:
            request_data['order'] = order
        
        result = await self._make_request('POST', 'crm.deal.list', request_data)
        
        deals_data = result.get('result', [])
        
        return [Bitrix24Deal(deal_data) for deal_data in deals_data]
    
    async def search_deals(
        self,
        search_query: str,
        limit: int = 20
    ) -> List[Bitrix24Deal]:
        """
        Поиск сделок по тексту.
        
        Args:
            search_query: Поисковый запрос
            limit: Максимальное количество результатов
            
        Returns:
            Список найденных сделок
        """
        filter_params = {
            '%TITLE': search_query  # Поиск по названию
        }
        
        return await self.list_deals(
            filter_params=filter_params,
            limit=limit,
            order={'DATE_MODIFY': 'DESC'}
        )
    
    async def get_deals_by_stage(
        self,
        stage_id: str,
        limit: int = 50
    ) -> List[Bitrix24Deal]:
        """
        Получение сделок по стадии.
        
        Args:
            stage_id: ID стадии
            limit: Максимальное количество сделок
            
        Returns:
            Список сделок в указанной стадии
        """
        filter_params = {'STAGE_ID': stage_id}
        
        return await self.list_deals(
            filter_params=filter_params,
            limit=limit,
            order={'DATE_MODIFY': 'DESC'}
        )
    
    async def get_deals_by_contact(
        self,
        contact_id: Union[int, str],
        limit: int = 50
    ) -> List[Bitrix24Deal]:
        """
        Получение сделок по контакту.
        
        Args:
            contact_id: ID контакта
            limit: Максимальное количество сделок
            
        Returns:
            Список сделок контакта
        """
        filter_params = {'CONTACT_ID': str(contact_id)}
        
        return await self.list_deals(
            filter_params=filter_params,
            limit=limit,
            order={'DATE_CREATE': 'DESC'}
        )
    
    async def get_deals_by_company(
        self,
        company_id: Union[int, str],
        limit: int = 50
    ) -> List[Bitrix24Deal]:
        """
        Получение сделок по компании.
        
        Args:
            company_id: ID компании
            limit: Максимальное количество сделок
            
        Returns:
            Список сделок компании
        """
        filter_params = {'COMPANY_ID': str(company_id)}
        
        return await self.list_deals(
            filter_params=filter_params,
            limit=limit,
            order={'DATE_CREATE': 'DESC'}
        )
    
    async def get_open_deals(self, limit: int = 50) -> List[Bitrix24Deal]:
        """
        Получение открытых сделок.
        
        Args:
            limit: Максимальное количество сделок
            
        Returns:
            Список открытых сделок
        """
        filter_params = {'CLOSED': 'N'}
        
        return await self.list_deals(
            filter_params=filter_params,
            limit=limit,
            order={'DATE_MODIFY': 'DESC'}
        )
    
    async def get_closed_deals(self, limit: int = 50) -> List[Bitrix24Deal]:
        """
        Получение закрытых сделок.
        
        Args:
            limit: Максимальное количество сделок
            
        Returns:
            Список закрытых сделок
        """
        filter_params = {'CLOSED': 'Y'}
        
        return await self.list_deals(
            filter_params=filter_params,
            limit=limit,
            order={'DATE_MODIFY': 'DESC'}
        )
    
    async def close_deal(
        self,
        deal_id: Union[int, str],
        stage_id: str = 'WON'
    ) -> Bitrix24Deal:
        """
        Закрытие сделки.
        
        Args:
            deal_id: ID сделки
            stage_id: ID финальной стадии (по умолчанию 'WON')
            
        Returns:
            Закрытая сделка
        """
        update_data = {
            'STAGE_ID': stage_id,
            'CLOSED': 'Y'
        }
        
        return await self.update_deal(deal_id, update_data)


# Вспомогательные функции для быстрого использования

async def create_quick_deal(
    webhook_url: str,
    title: str,
    opportunity: float,
    stage_id: str = 'NEW',
    **kwargs
) -> Bitrix24Deal:
    """
    Быстрое создание сделки без создания API клиента.
    
    Args:
        webhook_url: URL webhook Bitrix24
        title: Название сделки
        opportunity: Сумма сделки
        stage_id: ID стадии
        **kwargs: Дополнительные параметры сделки
        
    Returns:
        Созданная сделка
    """
    deal_data = {
        'TITLE': title,
        'OPPORTUNITY': opportunity,
        'STAGE_ID': stage_id,
        **kwargs
    }
    
    async with Bitrix24DealsAPI(webhook_url) as api:
        return await api.create_deal(deal_data)


async def get_deal_info(
    webhook_url: str,
    deal_id: Union[int, str]
) -> Optional[Bitrix24Deal]:
    """
    Быстрое получение информации о сделке.
    
    Args:
        webhook_url: URL webhook Bitrix24
        deal_id: ID сделки
        
    Returns:
        Информация о сделке или None
    """
    async with Bitrix24DealsAPI(webhook_url) as api:
        return await api.get_deal(deal_id)
