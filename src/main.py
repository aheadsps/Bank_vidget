import os
from typing import List, Dict, Optional

from decorators import log
from finance_reader import read_csv_transactions, read_excel_transactions
from utils import read_json
from processing import filter_by_state, sort_by_date
from processing_operations import process_bank_search
from generators import filter_by_currency
from external_api import convert_currency_to_rub
from widget import mask_account_card, get_date

@log(filename="logs/main.log")
def process_transactions(
    transactions: List[Dict],
    state: str,
    sort_by_date_flag: bool,
    sort_ascending: bool,
    rub_only: bool,
    search_string: Optional[str]
) -> List[Dict]:
    """Обрабатывает транзакции с учётом фильтров пользователя."""
    # Фильтрация по статусу
    filtered = filter_by_state(transactions, state.upper())

    # Сортировка по дате
    if sort_by_date_flag:
        filtered = sort_by_date(filtered, order=sort_ascending)

    # Фильтрация по рублям
    if rub_only:
        filtered = list(filter_by_currency(filtered, "RUB"))

    # Поиск по строке
    if search_string:
        filtered = process_bank_search(filtered, search_string)

    return filtered

def format_transaction(transaction: Dict) -> str:
    """
    Форматирует транзакцию для вывода.
    """
    # Форматирование даты
    date = get_date(transaction.get("date", "")) or "N/A"
    date = date.split(' (')[1][1:-2] if date else "N/A"  # Извлекаем ДД.ММ.ГГГГ

    # Описание
    description = transaction.get("description", "N/A")

    # От кого и кому
    from_acc = transaction.get("from", "")
    to_acc = transaction.get("to", "")
    from_formatted = mask_account_card(from_acc) if from_acc else "N/A"
    to_formatted = mask_account_card(to_acc) if to_acc else "N/A"
    accounts = f"{from_formatted} -> {to_formatted}" if from_acc else to_formatted

    # Сумма и валюта
    amount = float(transaction.get("operationAmount", {}).get("amount", 0))
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("code", "N/A")
    if currency != "RUB":
        amount_rub = convert_currency_to_rub(transaction)
        amount_str = f"{amount} {currency}" if amount_rub is None else f"{amount_rub:.2f} руб."
    else:
        amount_str = f"{amount:.2f} руб."

    return f"{date} {description}\n{accounts}\nСумма: {amount_str}\n"

def main():
    """
    Основная функция программы, реализующая пользовательский интерфейс и логику.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Выбор источника данных
    choice = input().strip()
    file_path = ""
    if choice == "1":
        file_path = os.path.join("data", "operations.json")
        print("Для обработки выбран JSON-файл.")
        transactions = read_json(file_path)
    elif choice == "2":
        file_path = os.path.join("data", "transactions.csv")
        print("Для обработки выбран CSV-файл.")
        transactions = read_csv_transactions(file_path)
    elif choice == "3":
        file_path = os.path.join("data", "transactions_excel.xlsx")
        print("Для обработки выбран XLSX-файл.")
        transactions = read_excel_transactions(file_path)
    else:
        print("Неверный выбор. Завершение программы.")
        return

    if not transactions:
        print("Не удалось загрузить транзакции. Завершение программы.")
        return

    # Фильтрация по статусу
    valid_states = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        state = input().strip().upper()
        if state in valid_states:
            print(f'Операции отфильтрованы по статусу "{state}"')
            break
        print(f'Статус операции "{state}" недоступен.')

    # Сортировка по дате
    print("\nОтсортировать операции по дате? Да/Нет")
    sort_by_date_flag = input().strip().lower() == "да"

    sort_ascending = True
    if sort_by_date_flag:
        print("Отсортировать по возрастанию или по убыванию?")
        sort_ascending = input().strip().lower() == "по возрастанию"

    # Фильтрация по рублям
    print("\nВыводить только рублевые транзакции? Да/Нет")
    rub_only = input().strip().lower() == "да"

    # Поиск по описанию
    search_string = None
    print("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет")
    if input().strip().lower() == "да":
        print("Введите слово для поиска:")
        search_string = input().strip()

    # Обработка транзакций
    filtered_transactions = process_transactions(
        transactions, state, sort_by_date_flag, sort_ascending, rub_only, search_string
    )

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")
    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(filtered_transactions)}\n")
    for transaction in filtered_transactions:
        print(format_transaction(transaction))

if __name__ == "__main__":
    main()