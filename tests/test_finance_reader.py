from datetime import date
from unittest.mock import patch

from src.finance_reader import read_csv_transactions, read_excel_transactions

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

@patch("pandas.read_csv")
def test_read_csv_transactions(mock_csv):
    mock_csv.return_value.to_dict.return_value = SAMPLE_TRANSACTIONS
    result = read_csv_transactions('test_csv')
    assert result == SAMPLE_TRANSACTIONS


@patch("pandas.read_excel")
def test_read_excel_transactions(mock_excel):
    mock_excel.return_value.to_dict.return_value = SAMPLE_TRANSACTIONS
    result = read_excel_transactions('test_excel')
    assert result == SAMPLE_TRANSACTIONS
