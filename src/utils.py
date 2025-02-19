import json
import os
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


def read_json(file_path: str) -> List[Dict[str, Any]]:
    """Функция, которая читает json файл и возвращает список словарей, либо в случае
    исключения выводит сообщение об ошибке"""
    try:
        # Открываем файл и читаем данные
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            return data
        else:
            print(f"Файл {file_path} не содержит список. Возвращаю пустой список.")
            return []

    # Отрабатываем иссключения
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    except json.decoder.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле: {file_path}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # Возвращаем пустой список в случае ошибок
    return []


def convert_currency_to_rub(transaction: Dict[str, Any]) -> Optional[float]:
    """Функция конвертирует сумму транзакции из USD или EUR в рубли (RUB)"""

    # Проверяем, что транзакция содержит необходимые ключи
    if "amount" not in transaction or "currency" not in transaction:
        print("Транзакция должна содержать ключи 'amount' и 'currency'")
        return None

    amount = transaction["amount"]
    currency = transaction["currency"].upper()  # Приводим валюту к верхнему регистру

    # Если валюта уже в рублях, возвращаем сумму без изменений
    if currency == "RUB":
        return float(amount)

    # Поддерживаемые валюты для конвертации
    if currency not in ["USD", "EUR"]:
        print(f"Валюта {currency} не поддерживается для конвертации")
        return None

    # Получаем API-ключ из .env
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        print("API-ключ не найден в файле .env")
        return None

    # ссылка для получения курсов валют (USD и EUR относительно RUB)
    url = "https://api.apilayer.com/exchangerates_data/latest?symbols=USD,EUR&base=RUB"

    try:
        # Отправляем GET-запрос с API-ключом в заголовке
        headers = {"apikey": api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверяем, что запрос успешен

        # Извлекаем курсы валют из ответа
        data = response.json()
        if "rates" not in data:
            print("Курсы валют не найдены в ответе API.")
            return None

        exchange_rates = data["rates"]

        # Конвертируем сумму в рубли
        if currency in exchange_rates:
            rate = exchange_rates[currency]
            converted_amount = amount * rate  # Конвертируем сумму в рубли
            return float(converted_amount)
        else:
            print(f"Курс для валюты {currency} не найден.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None


if __name__ == "__main__":
    # USD
    transaction_usd = {"amount": 100, "currency": "USD"}
    converted_amount_usd = convert_currency_to_rub(transaction_usd)
    if converted_amount_usd is not None:
        print(f"Сумма в рублях: {converted_amount_usd}")

    # EUR
    transaction_eur = {"amount": 50, "currency": "EUR"}
    converted_amount_eur = convert_currency_to_rub(transaction_eur)
    if converted_amount_eur is not None:
        print(f"Сумма в рублях: {converted_amount_eur}")

    # RUB
    transaction_rub = {"amount": 1000, "currency": "RUB"}
    converted_amount_rub = convert_currency_to_rub(transaction_rub)
    if converted_amount_rub is not None:
        print(f"Сумма в рублях: {converted_amount_rub}")

    # Транзакция с неподдерживаемой валютой
    transaction_gbp = {"amount": 200, "currency": "GBP"}
    converted_amount_gbp = convert_currency_to_rub(transaction_gbp)
    if converted_amount_gbp is None:
        print("Конвертация для GBP не поддерживается.")
