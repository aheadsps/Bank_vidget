def filter_by_state(dictionaries: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция, которая принимает список словарей с параметрами, и на основе значения state возвращет список словарей
    только с нужным значением"""
    result_list = []
    try:
        for dictionary in dictionaries:
            if dictionary["state"] == state:
                result_list.append(dictionary)
        return result_list
    except KeyError:
        raise Exception("список словарей неверен")


def sort_by_date(dictionaries: list[dict], order: bool = True) -> list[dict]:
    """Функция, которая принимает список словарей и за счёт необязательного параметра сортирует список по дате."""
    result = []
    try:
        for dictionary in dictionaries:
            if dictionary["date"].startswith("20") and len(dictionary["date"]) == 26:
                result.append(dictionary)
    except KeyError:
        raise Exception("список словарей неверен")
    else:
        result = sorted(result, key=lambda x: x["date"], reverse=order)
        return result
