from datetime import date
from unittest.mock import mock_open, patch

import pandas as pd
import pytest
from src.finance_reader import read_csv_transactions, read_excel_transactions

SAMPLE_CSV = """650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации
3598919;EXECUTED;2020-12-06T23:00:58Z;29740;Peso;COP;Discover 3172601889670065;Discover 0720428384694643;Перевод с карты на карту
;;;;;;;;
"""

SAMPLE_TRANSACTIONS = [
    {
        'id': 650703,
        'state': 'EXECUTED',
        'date': date(2023, 9, 5),
        'amount': 16210.0,
        'currency_name': 'Sol',
        'currency_code': 'PEN',
        'from': 'Счет 58803664561298323391',
        'to': 'Счет 39745660563456619397',
        'description': 'Перевод организации'
    },
    {
        'id': 3598919,
        'state': 'EXECUTED',
        'date': date(2020, 12, 6),
        'amount': 29740.0,
        'currency_name': 'Peso',
        'currency_code': 'COP',
        'from': 'Discover 3172601889670065',
        'to': 'Discover 0720428384694643',
        'description': 'Перевод с карты на карту'
    }
]

@pytest.fixture
def mock_csv_file():
    return SAMPLE_CSV

@pytest.fixture
def mock_excel_data():
    # Эмулируем Excel-файл с пропуском первой строки и пустой строкой
    return pd.DataFrame([
        {
            'id': 650703,
            'state': 'EXECUTED',
            'date': '2023-09-05T11:30:32Z',
            'amount': 16210.0,
            'currency_name': 'Sol',
            'currency_code': 'PEN',
            'from': 'Счет 58803664561298323391',
            'to': 'Счет 39745660563456619397',
            'description': 'Перевод организации'
        },
        {
            'id': 3598919,
            'state': 'EXECUTED',
            'date': '2020-12-06T23:00:58Z',
            'amount': 29740.0,
            'currency_name': 'Peso',
            'currency_code': 'COP',
            'from': 'Discover 3172601889670065',
            'to': 'Discover 0720428384694643',
            'description': 'Перевод с карты на карту'
        },
        {
            'id': None,
            'state': None,
            'date': None,
            'amount': None,
            'currency_name': None,
            'currency_code': None,
            'from': None,
            'to': None,
            'description': None
        }
    ])

@patch('builtins.open', new_callable=mock_open)
def test_read_csv_transactions(mock_file, mock_csv_file):
    mock_file.return_value.__enter__.return_value.read.return_value = mock_csv_file
    result = read_csv_transactions('test.csv')
    assert result == SAMPLE_TRANSACTIONS
    mock_file.assert_called_once_with('test.csv', 'r', encoding='utf-8')

@patch('builtins.open', new_callable=mock_open)
def test_read_csv_transactions_file_not_found(mock_file):
    mock_file.side_effect = FileNotFoundError
    with pytest.raises(FileNotFoundError):
        read_csv_transactions('nonexistent.csv')

@patch('pandas.read_excel')
def test_read_excel_transactions(mock_read_excel, mock_excel_data):
    mock_read_excel.return_value = mock_excel_data
    result = read_excel_transactions('test.xlsx')
    assert result == SAMPLE_TRANSACTIONS
    mock_read_excel.assert_called_once_with('test.xlsx', skiprows=1)

@patch('pandas.read_excel')
def test_read_excel_transactions_file_not_found(mock_read_excel):
    mock_read_excel.side_effect = FileNotFoundError
    with pytest.raises(FileNotFoundError):
        read_excel_transactions('nonexistent.xlsx')

def test_read_csv_transactions_invalid_data(mock_csv_file):
    invalid_csv = """1;EXECUTED;invalid_date;100.50;Sol;PEN;Account1;Account2;Test"""
    with patch('builtins.open', mock_open(read_data=invalid_csv)):
        result = read_csv_transactions('test.csv')
        assert len(result) == 0  # Пропускаем некорректную строку

def test_read_csv_transactions_empty_line(mock_csv_file):
    empty_line_csv = """650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации
;;;;;;;;
"""
    with patch('builtins.open', mock_open(read_data=empty_line_csv)):
        result = read_csv_transactions('test.csv')
        assert len(result) == 1  # Пропускаем пустую строку

def test_read_excel_transactions_invalid_data(mock_excel_data):
    mock_excel_data.iloc[0, 2] = 'invalid_date'  # Некорректный формат даты
    with patch('pandas.read_excel', return_value=mock_excel_data):
        result = read_excel_transactions('test.xlsx')
        assert len(result) == 1  # Пропускаем некорректную строку

def test_read_excel_transactions_empty_line(mock_excel_data):
    # Проверяем, что пустая строка (последняя) пропускается
    with patch('pandas.read_excel', return_value=mock_excel_data):
        result = read_excel_transactions('test.xlsx')
        assert len(result) == 2  # Пропускаем пустую строку