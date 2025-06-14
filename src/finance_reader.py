from typing import Dict, List

import pandas as pd


def read_csv_transactions(file_path: str) -> List[Dict]:
    """Функция открывает csv и отдает список словарей с транзакциями"""
    df = pd.read_csv(file_path, delimiter=";")
    return df.to_dict(orient="records")


def read_excel_transactions(file_path: str) -> List[Dict]:
    """Функция открывает excel и отдает список словарей с транзакциями"""
    df = pd.read_excel(file_path)
    return df.to_dict(orient="records")


# read_csv = read_csv_transactions('data/transactions.csv')
# print(read_csv)

# read_excel = read_excel_transactions('data/transactions_excel.xlsx')
# print(read_excel)
