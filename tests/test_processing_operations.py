import pytest
from src.processing_operations import process_bank_search, process_bank_operations

@pytest.fixture
def test_data():
    """Фикстура с тестовыми данными."""
    return [
        {'id': 1, 'description': 'Покупка в магазине'},
        {'id': 2, 'description': 'Оплата за интернет'},
        {'id': 3, 'description': 'Перевод другу'},
        {'id': 4, 'description': 'Покупка билетов'},
        {'id': 5, 'description': 'Оплата коммунальных услуг'},
        {'id': 6, 'description': ''},  # Пустое описание
        {'id': 7}  # Отсутствует поле description
    ]

@pytest.fixture
def categories():
    """Фикстура со списком категорий."""
    return ['покупка', 'оплата', 'перевод']

def test_process_bank_search_basic(test_data):
    """Тест поиска по строке 'покупка'."""
    result = process_bank_search(test_data, 'покупка')
    expected = [
        {'id': 1, 'description': 'Покупка в магазине'},
        {'id': 4, 'description': 'Покупка билетов'}
    ]
    assert result == expected

def test_process_bank_search_case_insensitive(test_data):
    """Тест поиска с игнорированием регистра."""
    result = process_bank_search(test_data, 'ПОКУПКА')
    expected = [
        {'id': 1, 'description': 'Покупка в магазине'},
        {'id': 4, 'description': 'Покупка билетов'}
    ]
    assert result == expected

def test_process_bank_search_no_matches(test_data):
    """Тест поиска с отсутствующей строкой."""
    result = process_bank_search(test_data, 'несуществующий')
    assert result == []

def test_process_bank_search_empty_description(test_data):
    """Тест поиска с пустой строкой"""
    result = process_bank_search(test_data, '')
    assert result == test_data

def test_process_bank_operations_basic(test_data, categories):
    """Тест подсчёта операций по категориям."""
    result = process_bank_operations(test_data, categories)
    expected = {
        'покупка': 2,
        'оплата': 2,
        'перевод': 1
    }
    assert result == expected

def test_process_bank_operations_empty_categories(test_data):
    """Тест с пустым списком категорий."""
    result = process_bank_operations(test_data, [])
    assert result == {}

def test_process_bank_operations_no_matches(test_data):
    """Тест с категориями, которых нет в данных."""
    result = process_bank_operations(test_data, ['несуществующий'])
    assert result == {'несуществующий': 0}

def test_process_bank_operations_empty_description(test_data):
    """Тест с пустым описанием и отсутствующим полем."""
    result = process_bank_operations(test_data, ['покупка'])
    assert result == {'покупка': 2}