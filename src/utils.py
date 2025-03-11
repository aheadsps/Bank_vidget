import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_json(file_path: str) -> List[Dict[str, Any]]:
    """Функция, которая читает json файл и возвращает список словарей, либо в случае
    исключения выводит сообщение об ошибке"""
    logger.info("Старт функции read_json")
    try:
        # Открываем файл и читаем данные
        with open(file_path, "r", encoding="utf-8") as json_file:
            logger.debug(f'файл открыт и записан во временную переменную json_file: {json_file}')
            data = json.load(json_file)
            logger.debug(f'файл переведен в json_file: {data}')


        # Проверяем, что данные являются списком
        if isinstance(data, list):
            logger.debug(f'проверка данных, что они список: {data}')
            logger.info("Успешное завершение функции read_json")
            return data
        else:
            logger.warning(f'Файл {file_path} не содержит список. Возвращаю пустой список.')
            print(f"Файл {file_path} не содержит список. Возвращаю пустой список.")
            return []

    # Отрабатываем иссключения
    except FileNotFoundError as ex:
        logger.error(f'Произошла ошибка: {ex}')
        print(f"Файл не найден: {file_path}")
        return []
    except json.decoder.JSONDecodeError as ex:
        logger.error(f'Произошла ошибка: {ex}')
        print(f"Ошибка декодирования JSON в файле: {file_path}")
        return []
    except Exception as ex:
        logger.error(f'Произошла ошибка: {ex}')
        print(f"Произошла ошибка: {ex}")
        return []
