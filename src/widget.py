from masks import get_mask_card_number
from masks import get_mask_account

test_input_string = str(input())


def mask_account_card(str_account_card: str) -> str:
    '''функция, которая принимает строку с названием и номером счета, карты
    и возвращает строку с названием и замаскированным номером счета/карты'''
    new_string_mask = ''
    if 'Счет' in str_account_card:
        new_string_mask += str_account_card[:-20] + (get_mask_account(str_account_card[-20:]))
    else:
        new_string_mask += str_account_card[:-16] + (get_mask_card_number(str_account_card[-16:]))
    return new_string_mask

print(mask_account_card(test_input_string))


