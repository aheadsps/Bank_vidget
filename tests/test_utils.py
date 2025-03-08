import os
import unittest
from unittest.mock import mock_open, patch

import pytest
from requests.exceptions import RequestException

from src.external_api import convert_currency_to_rub
from src.utils import read_json


# Тесты для функции read_json
def test_read_json_valid():
    """Тест для чтения корректного JSON-файла."""
    json_data = \
        ('[{"operationAmount": {"amount": "31957.58", "currency": {"code": "RUB"}}}, '
         '{"operationAmount": {"amount": "720983.07", "currency": {"code": "USD"}}}]')
    with patch("builtins.open", mock_open(read_data=json_data)):
        result = read_json("dummy_path.json")
        assert result == \
               [{"operationAmount": {"amount": "31957.58", "currency": {"code": "RUB"}}},
                {"operationAmount": {"amount": "720983.07", "currency": {"code": "USD"}}}]


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


@patch("requests.get")
def test_convert_currency_to_rub_usd(mock_get, positive_transactions_usd):
    """Тест для конвертации USD в RUB."""
    # Мок-ответ от API с курсами валют
    mock_response = {"rates": {"USD": 0.011403, "EUR": 0.010961}, "success": True}
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status.return_value = None

    # Вызов тестируемой функции
    result = convert_currency_to_rub(positive_transactions_usd)

    # Проверка результата
    assert result == 8769.622029290538

@patch("requests.get")
def test_convert_currency_to_rub_eur(mock_get, positive_transactions_eur):
    """Тест для конвертации EUR в RUB."""
    # Мок-ответ от API с курсами валют
    mock_response = {"rates": {"USD": 0.011403, "EUR": 0.010961}, "success": True}
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status.return_value = None

    # Вызов тестируемой функции
    result = convert_currency_to_rub(positive_transactions_eur)

    # Проверка результата
    assert result == 9123.255177447312

@patch("requests.get")
def test_convert_currency_to_rub_rub(mock_get, positive_transactions_rub):
    """Тест для случая, когда валюта уже в рублях."""
    # Мок-ответ от API с курсами валют
    mock_response = {"rates": {"USD": 0.011403, "EUR": 0.010961}, "success": True}
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status.return_value = None

    # Вызов тестируемой функции
    result = convert_currency_to_rub(positive_transactions_rub)

    # Проверка результата
    assert result == 100.0

if __name__ == "__main__":
    unittest.main()
