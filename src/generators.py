from typing import Iterator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """Функция, которая принимает на вход список словарей, представляющих транзакции
    и возвращает итератор, который поочередно выдает транзакции, где валюта операции
    соответствует заданной (например, USD)"""
    for dictionary in transactions:
        verify_code = dictionary["operationAmount"]["currency"]["code"]
        try:
            if verify_code.isalpha() and len(verify_code) > 2:
                return filter(lambda x: x["operationAmount"]["currency"]["code"] == currency, transactions)
        except KeyError:
            raise Exception("Данные списка словарей неверны")


def transaction_descriptions(transactions: list[dict]) -> Iterator[dict]:
    """Функция-генератор, которая принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди"""
    for description in transactions:
        verify_description = description.get("description")
        try:
            if verify_description.startswith("Перевод"):
                yield f"{verify_description}"
        except KeyError:
            raise Exception("Данные списка словарей неверны")


def card_number_generator(start_number: int, end_number: int) -> Iterator[str]:
    """Функция, которая принимает начальное и конечное значение номеров карт
    и генерирует номера карт от 0000 0000 0000 0001 до 9999 9999 9999 9999"""
    flag = True
    while flag:
        if start_number <= 0 or end_number <= 0 or start_number > end_number:
            yield "Неверные входные данные"
        if end_number >= 1 and start_number <= 0:
            yield "Неверные входные данные"
            start_number += 1
        else:
            flag = False

    for number in range(start_number, end_number + 1):
        generate_number = f"{number:016}"  # Формируем номер с ведущими нулями
        number_card = f"{generate_number[:4]} {generate_number[4:8]} {generate_number[8:12]} {generate_number[12:]}"
        yield number_card
