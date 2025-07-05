from typing import List, Dict, Tuple

import re


def process_bank_search(data:list[dict], search:str)->list[dict]:
    """Функция, которая принимает список словарей с данными о банковских операциях
    и строку поиска, а возвращает список словарей, у которых в описании есть
    данная строка."""

    pattern = re.compile(re.escape(search), re.IGNORECASE)

    return [item for item in data if pattern.search(item.get('description', ''))]


def process_bank_operations(data:list[dict], categories:list)->dict:
    """Функция, которая принимает список словарей с данными о банковских операциях
    и список категорий операций, а возвращает словарь, в котором ключи — это
    названия категорий, а значения — это количество операций в каждой категории."""

    # Инициализируем словарь для подсчёта операций по категориям
    result = {category: 0 for category in categories}

    # Проходим по каждой операции
    for item in data:
        description = item.get('description', '').lower()
        # Проверяем каждую категорию
        for category in categories:
            # Создаём паттерн для поиска категории (нечувствительный к регистру)
            pattern = re.compile(re.escape(category), re.IGNORECASE)
            if pattern.search(description):
                result[category] += 1

    return result


if __name__ == '__main__':
    # Тестовые данные
    bank_data = [
        {'id': 1, 'description': 'Покупка в магазине'},
        {'id': 2, 'description': 'Оплата за интернет'},
        {'id': 3, 'description': 'Перевод другу'},
        {'id': 4, 'description': 'Покупка билетов'},
        {'id': 5, 'description': 'Оплата коммунальных услуг'}
    ]

    # Тест для process_bank_search
    search_string = 'покупка'
    search_result = process_bank_search(bank_data, search_string)
    print(f"Результат поиска по '{search_string}':")
    for item in search_result:
        print(item)

    print("\n" + "=" * 50 + "\n")

    # Тест для process_bank_operations
    categories = ['покупка', 'оплата', 'перевод']
    operations_result = process_bank_operations(bank_data, categories)
    print("Результат подсчёта операций по категориям:")
    for category, count in operations_result.items():
        print(f"{category}: {count}")