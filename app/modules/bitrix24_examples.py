"""
Примеры использования API Bitrix24 для работы со сделками.

Этот файл содержит различные примеры использования Bitrix24DealsAPI
для демонстрации CRUD операций со сделками.
"""

import asyncio
from datetime import datetime
from app.modules.bitrix24_deals import Bitrix24DealsAPI, Bitrix24Deal, create_quick_deal, get_deal_info


# ВАЖНО: Замените на ваш реальный webhook URL
WEBHOOK_URL = "https://your-domain.bitrix24.ru/rest/1/your-webhook-code/"
USER_ID = 1  # Замените на ваш ID пользователя


async def example_create_deal():
    """Пример создания новой сделки."""
    print("=== Создание новой сделки ===")
    
    async with Bitrix24DealsAPI(WEBHOOK_URL, user_id=USER_ID) as api:
        deal_data = {
            'TITLE': f'Тестовая сделка {datetime.now().strftime("%Y-%m-%d %H:%M")}',
            'OPPORTUNITY': 100000,
            'CURRENCY_ID': 'RUB',
            'STAGE_ID': 'NEW',
            'COMMENTS': 'Это тестовая сделка, созданная через API'
        }
        
        try:
            deal = await api.create_deal(deal_data)
            print(f"Сделка создана: {deal}")
            print(f"ID: {deal.id}, Название: {deal.title}, Сумма: {deal.opportunity}")
            return deal.id
        except Exception as e:
            print(f"Ошибка создания сделки: {e}")
            return None


async def example_get_deal(deal_id: str):
    """Пример получения сделки по ID."""
    print(f"\n=== Получение сделки {deal_id} ===")
    
    async with Bitrix24DealsAPI(WEBHOOK_URL) as api:
        try:
            deal = await api.get_deal(deal_id)
            if deal:
                print(f"Сделка найдена: {deal}")
                print(f"Статус: {'Открыта' if deal.opened else 'Закрыта'}")
                print(f"Стадия: {deal.stage_id}")
                print(f"Дата создания: {deal.date_create}")
                return deal
            else:
                print("Сделка не найдена")
                return None
        except Exception as e:
            print(f"Ошибка получения сделки: {e}")
            return None


async def example_update_deal(deal_id: str):
    """Пример обновления сделки."""
    print(f"\n=== Обновление сделки {deal_id} ===")
    
    async with Bitrix24DealsAPI(WEBHOOK_URL) as api:
        update_data = {
            'TITLE': f'Обновленная сделка {datetime.now().strftime("%H:%M")}',
            'OPPORTUNITY': 150000,
            'COMMENTS': 'Сделка обновлена через API'
        }
        
        try:
            updated_deal = await api.update_deal(deal_id, update_data)
            print(f"Сделка обновлена: {updated_deal}")
            print(f"Новая сумма: {updated_deal.opportunity}")
            return updated_deal
        except Exception as e:
            print(f"Ошибка обновления сделки: {e}")
            return None


async def example_list_deals():
    """Пример получения списка сделок."""
    print("\n=== Список сделок ===")
    
    async with Bitrix24DealsAPI(WEBHOOK_URL) as api:
        try:
            # Получаем последние 10 сделок
            deals = await api.list_deals(
                order={'DATE_CREATE': 'DESC'},
                limit=10
            )
            
            print(f"Найдено сделок: {len(deals)}")
            for deal in deals:
                print(f"- {deal.id}: {deal.title} ({deal.opportunity} {deal.currency_id})")
            
            return deals
        except Exception as e:
            print(f"Ошибка получения списка сделок: {e}")
            return []


async def example_search_deals():
    """Пример поиска сделок."""
    print("\n=== Поиск сделок ===")
    
    async with Bitrix24DealsAPI(WEBHOOK_URL) as api:
        try:
            # Поиск сделок со словом "тест"
            deals = await api.search_deals("тест", limit=5)
            
            print(f"Найдено сделок с 'тест': {len(deals)}")
            for deal in deals:
                print(f"- {deal.id}: {deal.title}")
            
            return deals
        except Exception as e:
            print(f"Ошибка поиска сделок: {e}")
            return []


async def example_deals_by_stage():
    """Пример получения сделок по стадии."""
    print("\n=== Сделки по стадиям ===")
    
    async with Bitrix24DealsAPI(WEBHOOK_URL) as api:
        try:
            # Получаем новые сделки
            new_deals = await api.get_deals_by_stage('NEW', limit=5)
            print(f"Новых сделок: {len(new_deals)}")
            
            # Получаем открытые сделки
            open_deals = await api.get_open_deals(limit=5)
            print(f"Открытых сделок: {len(open_deals)}")
            
            # Получаем закрытые сделки
            closed_deals = await api.get_closed_deals(limit=5)
            print(f"Закрытых сделок: {len(closed_deals)}")
            
        except Exception as e:
            print(f"Ошибка получения сделок по стадиям: {e}")


async def example_close_deal(deal_id: str):
    """Пример закрытия сделки."""
    print(f"\n=== Закрытие сделки {deal_id} ===")
    
    async with Bitrix24DealsAPI(WEBHOOK_URL) as api:
        try:
            closed_deal = await api.close_deal(deal_id, stage_id='WON')
            print(f"Сделка закрыта: {closed_deal}")
            print(f"Статус: {'Закрыта' if closed_deal.closed else 'Открыта'}")
            return closed_deal
        except Exception as e:
            print(f"Ошибка закрытия сделки: {e}")
            return None


async def example_delete_deal(deal_id: str):
    """Пример удаления сделки."""
    print(f"\n=== Удаление сделки {deal_id} ===")
    
    async with Bitrix24DealsAPI(WEBHOOK_URL) as api:
        try:
            result = await api.delete_deal(deal_id)
            if result:
                print("Сделка успешно удалена")
            else:
                print("Не удалось удалить сделку")
            return result
        except Exception as e:
            print(f"Ошибка удаления сделки: {e}")
            return False


async def example_quick_functions():
    """Пример использования быстрых функций."""
    print("\n=== Быстрые функции ===")
    
    try:
        # Быстрое создание сделки
        deal = await create_quick_deal(
            webhook_url=WEBHOOK_URL,
            title="Быстрая сделка",
            opportunity=50000,
            stage_id='NEW',
            CURRENCY_ID='RUB'
        )
        print(f"Быстро создана сделка: {deal.id}")
        
        # Быстрое получение информации
        deal_info = await get_deal_info(WEBHOOK_URL, deal.id)
        if deal_info:
            print(f"Быстро получена информация: {deal_info.title}")
        
        return deal.id
        
    except Exception as e:
        print(f"Ошибка в быстрых функциях: {e}")
        return None


async def example_advanced_filtering():
    """Пример продвинутой фильтрации сделок."""
    print("\n=== Продвинутая фильтрация ===")
    
    async with Bitrix24DealsAPI(WEBHOOK_URL) as api:
        try:
            # Фильтр: сделки с суммой больше 50000 и в стадии NEW
            filter_params = {
                '>OPPORTUNITY': 50000,
                'STAGE_ID': 'NEW',
                'CLOSED': 'N'
            }
            
            deals = await api.list_deals(
                filter_params=filter_params,
                select_fields=['ID', 'TITLE', 'OPPORTUNITY', 'STAGE_ID'],
                order={'OPPORTUNITY': 'DESC'},
                limit=10
            )
            
            print(f"Найдено сделок по фильтру: {len(deals)}")
            for deal in deals:
                print(f"- {deal.id}: {deal.title} - {deal.opportunity} руб.")
                
        except Exception as e:
            print(f"Ошибка в продвинутой фильтрации: {e}")


async def full_crud_example():
    """Полный пример CRUD операций."""
    print("=== ПОЛНЫЙ ПРИМЕР CRUD ОПЕРАЦИЙ ===")
    
    try:
        # CREATE - Создание сделки
        deal_id = await example_create_deal()
        if not deal_id:
            print("Не удалось создать сделку, прерываем пример")
            return
        
        # READ - Чтение сделки
        deal = await example_get_deal(deal_id)
        if not deal:
            print("Не удалось получить сделку, прерываем пример")
            return
        
        # UPDATE - Обновление сделки
        updated_deal = await example_update_deal(deal_id)
        if not updated_deal:
            print("Не удалось обновить сделку")
        
        # Дополнительные операции
        await example_list_deals()
        await example_search_deals()
        await example_deals_by_stage()
        
        # Закрытие сделки
        await example_close_deal(deal_id)
        
        # DELETE - Удаление сделки (закомментировано для безопасности)
        # await example_delete_deal(deal_id)
        
        print("\n=== CRUD операции завершены ===")
        
    except Exception as e:
        print(f"Ошибка в полном примере: {e}")


async def main():
    """Главная функция для запуска примеров."""
    print("Запуск примеров работы с Bitrix24 API")
    print("ВНИМАНИЕ: Убедитесь, что указали правильный WEBHOOK_URL!")
    print("-" * 60)
    
    # Проверяем, что webhook URL изменен
    if "your-domain" in WEBHOOK_URL or "your-webhook-code" in WEBHOOK_URL:
        print("❌ ОШИБКА: Необходимо указать реальный webhook URL!")
        print("Измените переменную WEBHOOK_URL в начале файла")
        return
    
    await full_crud_example()
    
    # Запуск дополнительных примеров
    await example_quick_functions()
    await example_advanced_filtering()


if __name__ == '__main__':
    asyncio.run(main())
