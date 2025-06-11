import csv
import pandas as pd
from datetime import datetime


def read_csv_transactions(file_path):
    """
    Функция чтения транзакций из файла CSV.
    На вход принимает путь к файлу и возвращает список словарей с транзакциями.
    """

    transactions = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            next(file)

            fieldnames = ['id', 'state', 'date', 'amount', 'currency_name', 'currency_code', 'from', 'to',
                          'description']
            reader = csv.DictReader(file, fieldnames=fieldnames, delimiter=';')
            for row in reader:
                # Проверка пустых строк
                if not any(row.values()) or all(value.strip() == '' for value in row.values()):
                    continue

                try:
                    # Преобразуем данные в нужный формат
                    transaction = {
                        'id': int(row['id']),
                        'state': row['state'],
                        'date': datetime.strptime(row['date'], '%Y-%m-%dT%H:%M:%SZ').date(),
                        'amount': float(row['amount']),
                        'currency_name': row['currency_name'],
                        'currency_code': row['currency_code'],
                        'from': row['from'],
                        'to': row['to'],
                        'description': row['description']
                    }
                    transactions.append(transaction)
                except (ValueError, KeyError) as e:
                    print(f"Ошибка обработки строки {row}: {e}")
                    continue
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except Exception as e:
        raise Exception(f"Ошибка чтения CSV-файла: {e}")

    return transactions


def read_excel_transactions(file_path):
    """
    Функция чтения транзакций из файла Excel.
    На вход принимает путь к файлу и возвращает список словарей с транзакциями.
    """
    transactions = []
    try:
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            if row.isna().all() or all(str(val).strip() == '' for val in row):
                continue
            try:
                transaction = {
                    'id': int(row['id']),
                    'state': row['state'],
                    'date': pd.to_datetime(row['date']).date(),
                    'amount': float(row['amount']),
                    'currency_name': row['currency_name'],
                    'currency_code': row['currency_code'],
                    'from': row['from'],
                    'to': row['to'],
                    'description': row['description']
                }
                transactions.append(transaction)
            except (ValueError, KeyError) as e:
                print(f"Ошибка обработки строки {row}: {e}")
                continue
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except Exception as e:
        raise Exception(f"Ошибка чтения Excel файла: {e}")

    return transactions


# read_csv = read_csv_transactions('data/transactions.csv')
# df_csv = pd.DataFrame(read_csv)
# print(df_csv.head())
#
# read_excel = read_excel_transactions('data/transactions_excel.xlsx')
# df_csv = pd.DataFrame(read_csv)
# print(df_csv.head())