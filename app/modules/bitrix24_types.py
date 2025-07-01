"""
Типы данных для API Bitrix24.

Этот файл содержит типы и интерфейсы для улучшения
типизации при работе с API Bitrix24.
"""

from typing import Any, Dict, List, Optional, Union, Literal, TypedDict
from datetime import datetime
from enum import Enum


# Основные типы данных
DealID = Union[int, str]
UserID = Union[int, str]
ContactID = Union[int, str]
CompanyID = Union[int, str]
CurrencyCode = str
StageID = str
WebhookURL = str


# Типы для статусов сделок
class DealStatus(str, Enum):
    """Статусы сделок в Bitrix24."""
    OPEN = "Y"
    CLOSED = "N"


class SortOrder(str, Enum):
    """Порядок сортировки."""
    ASC = "ASC"
    DESC = "DESC"


# Стандартные стадии сделок (могут отличаться в зависимости от воронки)
class StandardDealStages(str, Enum):
    """Стандартные стадии сделок."""
    NEW = "NEW"
    PREPARATION = "PREPARATION"  
    PREPAYMENT_INVOICE = "PREPAYMENT_INVOICE"
    EXECUTING = "EXECUTING"
    FINAL_INVOICE = "FINAL_INVOICE"
    WON = "WON"
    LOSE = "LOSE"


# Валюты
class Currency(str, Enum):
    """Поддерживаемые валюты."""
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


# Типизированные словари для данных сделок
class DealCreateData(TypedDict, total=False):
    """Данные для создания сделки."""
    TITLE: str
    OPPORTUNITY: Union[int, float]
    CURRENCY_ID: CurrencyCode
    STAGE_ID: StageID
    CONTACT_ID: ContactID
    COMPANY_ID: CompanyID
    ASSIGNED_BY_ID: UserID
    COMMENTS: str
    ADDITIONAL_INFO: str
    OPENED: str  # 'Y' или 'N'


class DealUpdateData(TypedDict, total=False):
    """Данные для обновления сделки."""
    TITLE: str
    OPPORTUNITY: Union[int, float]
    CURRENCY_ID: CurrencyCode
    STAGE_ID: StageID
    CONTACT_ID: ContactID
    COMPANY_ID: CompanyID
    ASSIGNED_BY_ID: UserID
    COMMENTS: str
    ADDITIONAL_INFO: str
    OPENED: str
    CLOSED: str


class DealFilterParams(TypedDict, total=False):
    """Параметры фильтрации сделок."""
    # Точное совпадение
    ID: DealID
    TITLE: str
    STAGE_ID: StageID
    CONTACT_ID: ContactID
    COMPANY_ID: CompanyID
    ASSIGNED_BY_ID: UserID
    CREATED_BY_ID: UserID
    CURRENCY_ID: CurrencyCode
    OPENED: str
    CLOSED: str
    
    # Поиск по подстроке (начинается с %)
    TITLE_LIKE: str  # %TITLE
    
    # Числовые сравнения (начинаются с > < >= <=)
    OPPORTUNITY_GT: Union[int, float]  # >OPPORTUNITY
    OPPORTUNITY_LT: Union[int, float]  # <OPPORTUNITY
    OPPORTUNITY_GTE: Union[int, float]  # >=OPPORTUNITY
    OPPORTUNITY_LTE: Union[int, float]  # <=OPPORTUNITY
    
    # Диапазоны дат
    DATE_CREATE_FROM: str  # >=DATE_CREATE
    DATE_CREATE_TO: str    # <=DATE_CREATE
    DATE_MODIFY_FROM: str  # >=DATE_MODIFY
    DATE_MODIFY_TO: str    # <=DATE_MODIFY


class DealSelectFields(TypedDict, total=False):
    """Поля для выборки в сделках."""
    basic_fields: List[Literal[
        'ID', 'TITLE', 'STAGE_ID', 'OPPORTUNITY', 'CURRENCY_ID',
        'CONTACT_ID', 'COMPANY_ID', 'ASSIGNED_BY_ID', 'CREATED_BY_ID',
        'DATE_CREATE', 'DATE_MODIFY', 'OPENED', 'CLOSED', 'COMMENTS'
    ]]


class DealOrderParams(TypedDict, total=False):
    """Параметры сортировки сделок."""
    ID: SortOrder
    TITLE: SortOrder
    STAGE_ID: SortOrder
    OPPORTUNITY: SortOrder
    DATE_CREATE: SortOrder
    DATE_MODIFY: SortOrder


# Ответы API
class BitrixAPIResponse(TypedDict):
    """Базовый ответ API Bitrix24."""
    result: Any
    total: Optional[int]
    next: Optional[int]
    time: Optional[Dict[str, float]]


class DealListResponse(BitrixAPIResponse):
    """Ответ API для списка сделок."""
    result: List[Dict[str, Any]]


class DealGetResponse(BitrixAPIResponse):
    """Ответ API для получения сделки."""
    result: Dict[str, Any]


class DealCreateResponse(BitrixAPIResponse):
    """Ответ API для создания сделки."""
    result: DealID


class DealUpdateResponse(BitrixAPIResponse):
    """Ответ API для обновления сделки."""
    result: bool


class DealDeleteResponse(BitrixAPIResponse):
    """Ответ API для удаления сделки."""
    result: bool


# Исключения
class Bitrix24APIError(Exception):
    """Базовая ошибка API Bitrix24."""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.error_code = error_code


class DealNotFoundError(Bitrix24APIError):
    """Ошибка - сделка не найдена."""
    pass


class InvalidDealDataError(Bitrix24APIError):
    """Ошибка - некорректные данные сделки."""
    pass


class WebhookError(Bitrix24APIError):
    """Ошибка webhook URL."""
    pass


# Утилитарные типы
RequestMethod = Literal['GET', 'POST', 'PUT', 'DELETE']
APIEndpoint = str

# Конфигурация клиента
class Bitrix24Config(TypedDict, total=False):
    """Конфигурация клиента Bitrix24."""
    webhook_url: WebhookURL
    user_id: Optional[UserID]
    timeout: float
    retry_attempts: int
    retry_delay: float


# Статистика и аналитика
class DealStatistics(TypedDict):
    """Статистика по сделкам."""
    total_count: int
    open_count: int
    closed_count: int
    won_count: int
    lost_count: int
    total_amount: float
    average_amount: float
    currency: CurrencyCode


class StageStatistics(TypedDict):
    """Статистика по стадиям."""
    stage_id: StageID
    stage_name: str
    deal_count: int
    total_amount: float
    average_amount: float


# Пагинация
class PaginationParams(TypedDict, total=False):
    """Параметры пагинации."""
    start: int
    limit: int


class PaginationInfo(TypedDict):
    """Информация о пагинации."""
    current_page: int
    total_pages: int
    items_per_page: int
    total_items: int
    has_next: bool
    has_prev: bool
