from typing import Union

# test_number = 7000792289606361


def get_mask_card_number(number_card: Union[int]) -> str:
    """Функиця, которая принимает номер карты и возвращает его маску
    в формате XXXX XX** **** XXXX"""
    number_card_str = str(number_card)
    number_card_mask = f'{number_card_str[0:4]} {number_card_str[4:6]}** **** {number_card_str[-4:]}'

    return number_card_mask


# print(get_mask_card_number(test_number))

# test_account = 73654108430135874305


def get_mask_account(account_number: Union[int]) -> str:
    """Функция, которая прнимает номер счёта и возвращает маску с последними 4 цифрами
    и звездочками перед ними"""
    account_number_str = str(account_number)
    account_number_masks = "**" + account_number_str[-4:]

    return account_number_masks


# print(get_mask_account(test_account))