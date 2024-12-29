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


# test_sort_by_date = [
#     {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#     {'id': 939719570, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#     {'id': 594226727, 'state': 'CANCELED', 'date': '12.09.2018T21:27:25.241689'},
#     {'id': 615064591, 'state': 'CANCELED', 'date': '14.10.18'}
# ]
#
# order = 'False'
# print(sort_by_date(test_sort_by_date))


# def sort_by_date(dictionaries: list[dict], order: bool = True) -> list[dict]:
#     """Функция, которая принимает список словарей и за счет необязательного параметра сортирует список по дате"""
#     if dictionaries["date"] in dictionaries and len(dictionaries["date"]) == 26 and dictionaries["date"][4] == '-':
#         result = sorted(dictionaries, key=lambda x: x["date"], reverse=order)
#         return result
#     else:
#         raise Exception("список словарей неверен")

# test = [
#     {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
# ]
#
# print(filter_by_state(test))
