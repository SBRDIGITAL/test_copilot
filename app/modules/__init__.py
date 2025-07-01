"""
Модули приложения.

Этот пакет содержит различные модули для работы приложения.
"""

from .aiohttp_client import AsyncHTTPClient, get, post, put, delete
from .bitrix24_deals import (
    Bitrix24DealsAPI,
    Bitrix24Deal,
    create_quick_deal,
    get_deal_info
)
from .types import (
    AsyncHTTPClientProtocol,
    HTTPMethod,
    URL,
    Headers,
    Params,
    JSONData,
    RequestData,
    Cookies,
    ClientConfig,
    TimeoutConfig
)
from .bitrix24_types import (
    DealID,
    UserID,
    ContactID,
    CompanyID,
    StageID,
    WebhookURL,
    DealCreateData,
    DealUpdateData,
    DealFilterParams,
    Bitrix24APIError,
    DealNotFoundError,
    InvalidDealDataError
)

__all__ = [
    # HTTP клиент
    'AsyncHTTPClient',
    'get',
    'post', 
    'put',
    'delete',
    
    # Bitrix24 API
    'Bitrix24DealsAPI',
    'Bitrix24Deal',
    'create_quick_deal',
    'get_deal_info',
    
    # HTTP типы
    'AsyncHTTPClientProtocol',
    'HTTPMethod',
    'URL',
    'Headers',
    'Params',
    'JSONData',
    'RequestData',
    'Cookies',
    'ClientConfig',
    'TimeoutConfig',
    
    # Bitrix24 типы
    'DealID',
    'UserID',
    'ContactID',
    'CompanyID',
    'StageID',
    'WebhookURL',
    'DealCreateData',
    'DealUpdateData',
    'DealFilterParams',
    'Bitrix24APIError',
    'DealNotFoundError',
    'InvalidDealDataError'
]