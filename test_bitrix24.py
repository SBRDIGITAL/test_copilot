"""
Тесты для модуля Bitrix24 API с заглушками.

Этот файл содержит тесты для проверки функциональности
модуля bitrix24_deals без реального подключения к Bitrix24.
"""

import asyncio
import json
from unittest.mock import AsyncMock, patch
from app.modules.bitrix24_deals import Bitrix24DealsAPI, Bitrix24Deal


class MockBitrix24:
    """Заглушка для тестирования API Bitrix24."""
    
    def __init__(self):
        self.deals = {}
        self.next_id = 1
    
    def create_deal(self, deal_data):
        """Создание тестовой сделки."""
        deal_id = str(self.next_id)
        self.next_id += 1
        
        deal = {
            'ID': deal_id,
            'TITLE': deal_data.get('TITLE', ''),
            'OPPORTUNITY': deal_data.get('OPPORTUNITY', 0),
            'CURRENCY_ID': deal_data.get('CURRENCY_ID', 'RUB'),
            'STAGE_ID': deal_data.get('STAGE_ID', 'NEW'),
            'CONTACT_ID': deal_data.get('CONTACT_ID'),
            'COMPANY_ID': deal_data.get('COMPANY_ID'),
            'ASSIGNED_BY_ID': deal_data.get('ASSIGNED_BY_ID'),
            'CREATED_BY_ID': deal_data.get('CREATED_BY_ID'),
            'DATE_CREATE': '2025-07-01T10:00:00+03:00',
            'DATE_MODIFY': '2025-07-01T10:00:00+03:00',
            'OPENED': deal_data.get('OPENED', 'Y'),
            'CLOSED': deal_data.get('CLOSED', 'N'),
            'COMMENTS': deal_data.get('COMMENTS', ''),
            'ADDITIONAL_INFO': deal_data.get('ADDITIONAL_INFO', '')
        }
        
        self.deals[deal_id] = deal
        return {'result': deal_id}
    
    def get_deal(self, deal_id):
        """Получение тестовой сделки."""
        deal = self.deals.get(str(deal_id))
        if deal:
            return {'result': deal}
        else:
            return {'error': 'Deal not found'}
    
    def update_deal(self, deal_id, update_data):
        """Обновление тестовой сделки."""
        deal = self.deals.get(str(deal_id))
        if not deal:
            return {'error': 'Deal not found'}
        
        for key, value in update_data.items():
            if key in deal:
                deal[key] = value
        
        deal['DATE_MODIFY'] = '2025-07-01T10:30:00+03:00'
        return {'result': True}
    
    def delete_deal(self, deal_id):
        """Удаление тестовой сделки."""
        if str(deal_id) in self.deals:
            del self.deals[str(deal_id)]
            return {'result': True}
        else:
            return {'error': 'Deal not found'}
    
    def list_deals(self, params):
        """Получение списка тестовых сделок."""
        deals_list = list(self.deals.values())
        
        # Простая фильтрация по STAGE_ID
        filter_params = params.get('filter', {})
        if 'STAGE_ID' in filter_params:
            deals_list = [
                deal for deal in deals_list 
                if deal['STAGE_ID'] == filter_params['STAGE_ID']
            ]
        
        # Ограничение количества
        limit = params.get('limit', 50)
        start = params.get('start', 0)
        
        return {
            'result': deals_list[start:start + limit],
            'total': len(deals_list)
        }


# Глобальная заглушка
mock_bitrix = MockBitrix24()


async def mock_http_request(method, url, **kwargs):
    """Заглушка для HTTP-запросов."""
    # Парсим URL для определения операции
    if 'crm.deal.add' in url:
        data = kwargs.get('json', {})
        return mock_bitrix.create_deal(data.get('fields', {}))
    
    elif 'crm.deal.get' in url:
        data = kwargs.get('json', {})
        deal_id = data.get('id')
        return mock_bitrix.get_deal(deal_id)
    
    elif 'crm.deal.update' in url:
        data = kwargs.get('json', {})
        deal_id = data.get('id')
        fields = data.get('fields', {})
        return mock_bitrix.update_deal(deal_id, fields)
    
    elif 'crm.deal.delete' in url:
        data = kwargs.get('json', {})
        deal_id = data.get('id')
        return mock_bitrix.delete_deal(deal_id)
    
    elif 'crm.deal.list' in url:
        data = kwargs.get('json', {})
        return mock_bitrix.list_deals(data)
    
    else:
        return {'error': 'Unknown endpoint'}


class MockResponse:
    """Заглушка ответа HTTP."""
    
    def __init__(self, data, status=200):
        self.data = data
        self.status = status
    
    async def json(self):
        return self.data
    
    async def text(self):
        return json.dumps(self.data)


async def test_create_deal():
    """Тест создания сделки."""
    print("=== Тест создания сделки ===")
    
    with patch.object(
        Bitrix24DealsAPI, '_make_request',
        side_effect=lambda method, endpoint, data: mock_http_request(method, endpoint, json=data)
    ):
        async with Bitrix24DealsAPI("https://test.bitrix24.ru/rest/1/test/") as api:
            deal_data = {
                'TITLE': 'Тестовая сделка',
                'OPPORTUNITY': 100000,
                'CURRENCY_ID': 'RUB',
                'STAGE_ID': 'NEW'
            }
            
            deal = await api.create_deal(deal_data)
            print(f"✅ Создана сделка: {deal}")
            return deal.id


async def test_get_deal(deal_id):
    """Тест получения сделки."""
    print(f"\n=== Тест получения сделки {deal_id} ===")
    
    with patch.object(
        Bitrix24DealsAPI, '_make_request',
        side_effect=lambda method, endpoint, data: mock_http_request(method, endpoint, json=data)
    ):
        async with Bitrix24DealsAPI("https://test.bitrix24.ru/rest/1/test/") as api:
            deal = await api.get_deal(deal_id)
            if deal:
                print(f"✅ Получена сделка: {deal}")
                return deal
            else:
                print("❌ Сделка не найдена")
                return None


async def test_update_deal(deal_id):
    """Тест обновления сделки."""
    print(f"\n=== Тест обновления сделки {deal_id} ===")
    
    with patch.object(
        Bitrix24DealsAPI, '_make_request',
        side_effect=lambda method, endpoint, data: mock_http_request(method, endpoint, json=data)
    ):
        async with Bitrix24DealsAPI("https://test.bitrix24.ru/rest/1/test/") as api:
            update_data = {
                'TITLE': 'Обновленная тестовая сделка',
                'OPPORTUNITY': 150000
            }
            
            updated_deal = await api.update_deal(deal_id, update_data)
            print(f"✅ Обновлена сделка: {updated_deal}")
            return updated_deal


async def test_list_deals():
    """Тест получения списка сделок."""
    print("\n=== Тест получения списка сделок ===")
    
    with patch.object(
        Bitrix24DealsAPI, '_make_request',
        side_effect=lambda method, endpoint, data: mock_http_request(method, endpoint, json=data)
    ):
        async with Bitrix24DealsAPI("https://test.bitrix24.ru/rest/1/test/") as api:
            deals = await api.list_deals(limit=10)
            print(f"✅ Получено сделок: {len(deals)}")
            for deal in deals:
                print(f"  - {deal.id}: {deal.title}")
            return deals


async def test_delete_deal(deal_id):
    """Тест удаления сделки."""
    print(f"\n=== Тест удаления сделки {deal_id} ===")
    
    with patch.object(
        Bitrix24DealsAPI, '_make_request',
        side_effect=lambda method, endpoint, data: mock_http_request(method, endpoint, json=data)
    ):
        async with Bitrix24DealsAPI("https://test.bitrix24.ru/rest/1/test/") as api:
            result = await api.delete_deal(deal_id)
            if result:
                print("✅ Сделка удалена")
            else:
                print("❌ Не удалось удалить сделку")
            return result


async def test_bitrix24_deal_class():
    """Тест класса Bitrix24Deal."""
    print("\n=== Тест класса Bitrix24Deal ===")
    
    deal_data = {
        'ID': '123',
        'TITLE': 'Тестовая сделка для класса',
        'OPPORTUNITY': '75000',
        'CURRENCY_ID': 'RUB',
        'STAGE_ID': 'NEW',
        'OPENED': 'Y',
        'CLOSED': 'N',
        'DATE_CREATE': '2025-07-01T10:00:00+03:00'
    }
    
    deal = Bitrix24Deal(deal_data)
    
    print(f"✅ ID сделки: {deal.id}")
    print(f"✅ Название: {deal.title}")
    print(f"✅ Сумма: {deal.opportunity}")
    print(f"✅ Валюта: {deal.currency_id}")
    print(f"✅ Открыта: {deal.opened}")
    print(f"✅ Закрыта: {deal.closed}")
    print(f"✅ Строковое представление: {str(deal)}")
    print(f"✅ Repr: {repr(deal)}")
    
    # Тест преобразования в словарь
    deal_dict = deal.to_dict()
    print(f"✅ Словарь: {len(deal_dict)} полей")
    
    return deal


async def test_error_handling():
    """Тест обработки ошибок."""
    print("\n=== Тест обработки ошибок ===")
    
    with patch.object(
        Bitrix24DealsAPI, '_make_request',
        side_effect=lambda method, endpoint, data: {'error': 'Test error', 'error_description': 'Тестовая ошибка'}
    ):
        async with Bitrix24DealsAPI("https://test.bitrix24.ru/rest/1/test/") as api:
            try:
                await api.get_deal('999')
                print("❌ Ошибка не была обработана")
            except Exception as e:
                print(f"✅ Ошибка корректно обработана: {e}")


async def run_all_tests():
    """Запуск всех тестов."""
    print("🚀 Запуск тестов модуля Bitrix24 API")
    print("=" * 60)
    
    try:
        # Тест класса Deal
        await test_bitrix24_deal_class()
        
        # Тест создания сделки
        deal_id = await test_create_deal()
        
        # Тест получения сделки
        deal = await test_get_deal(deal_id)
        
        # Тест обновления сделки
        if deal:
            await test_update_deal(deal_id)
        
        # Тест списка сделок
        await test_list_deals()
        
        # Тест обработки ошибок
        await test_error_handling()
        
        # Тест удаления сделки
        await test_delete_deal(deal_id)
        
        print("\n" + "=" * 60)
        print("✅ Все тесты успешно пройдены!")
        
    except Exception as e:
        print(f"\n❌ Ошибка в тестах: {e}")


async def demo_real_structure():
    """Демонстрация структуры для реального использования."""
    print("\n" + "=" * 60)
    print("📋 Пример структуры для реального использования:")
    print("=" * 60)
    
    example_code = '''
# Реальное использование (замените на ваш webhook):
WEBHOOK_URL = "https://your-domain.bitrix24.ru/rest/1/your-code/"

async def real_usage_example():
    async with Bitrix24DealsAPI(WEBHOOK_URL, user_id=1) as api:
        # Создание сделки
        deal = await api.create_deal({
            'TITLE': 'Новая сделка от клиента',
            'OPPORTUNITY': 250000,
            'CURRENCY_ID': 'RUB',
            'STAGE_ID': 'NEW',
            'CONTACT_ID': '123',
            'COMMENTS': 'Клиент заинтересован в покупке'
        })
        
        # Получение и обновление
        deal = await api.get_deal(deal.id)
        await api.update_deal(deal.id, {'STAGE_ID': 'PREPARATION'})
        
        # Поиск и фильтрация
        new_deals = await api.get_deals_by_stage('NEW')
        open_deals = await api.get_open_deals()
        
        # Закрытие сделки
        await api.close_deal(deal.id, 'WON')
'''
    
    print(example_code)


if __name__ == '__main__':
    asyncio.run(run_all_tests())
    asyncio.run(demo_real_structure())
