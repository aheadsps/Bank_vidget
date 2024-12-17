from typing import Union

# test_number = 7000792289606361


def get_mask_card_number(number_card: int) -> str:
    """Функиця, которая принимает номер карты и возвращает его маску
    в формате XXXX XX** **** XXXX"""
    if len(str(number_card)) == 16 and number_card > 0 and isinstance(number_card, int):
        number_card_str = str(number_card)
        return f"{number_card_str[:4]} {number_card_str[4:6]}** **** {number_card_str[-4:]}"
    else:
        raise Exception("Номер карты не верен")


# print(get_mask_card_number(test_number))

# test_account = 73654108430135874305


def get_mask_account(account_number: int) -> str:
    """Функция, которая прнимает номер счёта и возвращает маску с последними 4 цифрами
    и звездочками перед ними"""
    if len(str(account_number)) == 20 and account_number > 0 and isinstance(account_number, int):
        account_number_str = str(account_number)
        return f"**{account_number_str[-4:]}"
    else:
        raise Exception("Номер счета не верен")


# print(get_mask_account(test_account))

# def get_mask_account(account_number: int) -> str:
#     """Принимает на вход номер счета (20цифр)
#     и возвращает его маску в формате **XXXX"""
#
#     if len(str(account_number)) == 20 and account_number > 0 and isinstance(account_number, int):
#         return f"**{str(account_number)[-4:]}"
#     else:
#         raise Exception("Номер счета должен состоять из 20 цифр")
