from masks import get_mask_account, get_mask_card_number

test_input_string = str(input())


def mask_account_card(str_account_card: str) -> str:
    """функция, которая принимает строку с названием и номером счета, карты
    и возвращает строку с названием и замаскированным номером счета/карты"""
    new_string_mask = ""
    if "Счет" in str_account_card:
        new_string_mask += str_account_card[:-20] + (get_mask_account(str_account_card[-20:]))
    else:
        new_string_mask += str_account_card[:-16] + (get_mask_card_number(str_account_card[-16:]))
    return new_string_mask


print(mask_account_card(test_input_string))

test_date_input = str(input())


def get_date(date_and_time_str: str) -> str:
    """функция, которая принимает строку в формате "2024-03-11T02:26:18.671407"
    и возвращает строку в формате "ДД.ММ.ГГГГ" ( "11.03.2024" )."""
    date_mask = f"{date_and_time_str[8:10]}.{date_and_time_str[5:7]}.{date_and_time_str[0:4]}"
    dd_mm_gg_masks = f' "ДД.ММ.ГГГГ" ( "{date_mask}" )'
    return dd_mm_gg_masks


print(get_date(test_date_input))
