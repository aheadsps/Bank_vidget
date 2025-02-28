import json
from typing import Any, Dict, List


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
