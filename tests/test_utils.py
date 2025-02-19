import os
from unittest.mock import mock_open, patch

import pytest
from requests.exceptions import RequestException

from src.utils import convert_currency_to_rub, read_json


# Тесты для функции read_json
def test_read_json_valid():
    """Тест для чтения корректного JSON-файла."""
    json_data = '[{"id": 1, "amount": 100, "currency": "USD"}]'
    with patch("builtins.open", mock_open(read_data=json_data)):
        result = read_json("dummy_path.json")
        assert result == [{"id": 1, "amount": 100, "currency": "USD"}]


def test_read_json_invalid():
    """Тест для чтения некорректного JSON-файла."""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        result = read_json("dummy_path.json")
        assert result == []


def test_read_json_not_found():
    """Тест для случая, когда файл не найден."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_json("nonexistent_path.json")
        assert result == []


def test_read_json_not_a_list():
    """Тест для случая, когда JSON-файл не содержит список."""
    json_data = '{"id": 1, "amount": 100, "currency": "USD"}'
    with patch("builtins.open", mock_open(read_data=json_data)):
        result = read_json("dummy_path.json")
        assert result == []


# Тесты для функции convert_currency_to_rub
@patch("requests.get")
def test_convert_currency_to_rub_usd(mock_get):
    """Тест для конвертации USD в RUB."""
    mock_response = {"rates": {"USD": 75.0, "EUR": 85.0}, "success": True}
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status.return_value = None

    transaction = {"amount": 100, "currency": "USD"}
    result = convert_currency_to_rub(transaction)
    assert result == 7500.0


@patch("requests.get")
def test_convert_currency_to_rub_eur(mock_get):
    """Тест для конвертации EUR в RUB."""
    mock_response = {"rates": {"USD": 75.0, "EUR": 85.0}, "success": True}
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status.return_value = None

    transaction = {"amount": 50, "currency": "EUR"}
    result = convert_currency_to_rub(transaction)
    assert result == 4250.0


def test_convert_currency_to_rub_rub():
    """Тест для случая, когда валюта уже в RUB."""
    transaction = {"amount": 1000, "currency": "RUB"}
    result = convert_currency_to_rub(transaction)
    assert result == 1000.0


def test_convert_currency_to_rub_invalid_currency():
    """Тест для случая, когда валюта не поддерживается."""
    transaction = {"amount": 200, "currency": "GBP"}
    result = convert_currency_to_rub(transaction)
    assert result is None


@patch("requests.get")
def test_convert_currency_to_rub_api_error(mock_get):
    """Тест для случая, когда API возвращает ошибку."""
    mock_get.side_effect = RequestException("API Error")
    transaction = {"amount": 100, "currency": "USD"}
    result = convert_currency_to_rub(transaction)
    assert result is None


def test_convert_currency_to_rub_missing_keys():
    """Тест для случая, когда в транзакции отсутствуют необходимые ключи."""
    transaction = {"amount": 100}  # Нет ключа 'currency'
    result = convert_currency_to_rub(transaction)
    assert result is None
