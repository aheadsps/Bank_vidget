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
        return []
    except json.decoder.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле: {file_path}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


def convert_currency_to_rub(transaction: Dict[str, Any]) -> Optional[float]:
    """Функция конвертирует сумму транзакции из USD или EUR в рубли (RUB)"""

    # Проверяем, что транзакция содержит необходимые ключи
    if "amount" not in transaction["operationAmount"] or "currency" not in transaction["operationAmount"]:
        print("Транзакция должна содержать ключи 'amount' и 'currency'")
        return None

    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"].upper()  # Приводим валюту к верхнему регистру

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
        # print(data)
        if "rates" not in data:
            print("Курсы валют не найдены в ответе API.")
            return None

        exchange_rates = data["rates"]

        # Конвертируем сумму в рубли
        if currency in exchange_rates:
            rate = exchange_rates[currency]
            converted_amount = amount / rate  # Конвертируем сумму в рубли
            return float(converted_amount)
        else:
            print(f"Курс для валюты {currency} не найден.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None


if __name__ == "__main__":
    file_path_total = os.path.join('data', 'operations.json')
    transactions = read_json(file_path_total)
    for transact in transactions[1:2]:
        result = convert_currency_to_rub(transact)
        print(f"Сумма в рублях: {result}")
