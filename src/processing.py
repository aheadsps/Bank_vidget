def filter_by_state(dictionaries: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция, которая принимает список словарей с параметрами, и на основе значения state возвращет список словарей
    только с нужным значением"""
    result_list = []
    for dictionary in dictionaries:
        if dictionary["state"] == state:
            result_list.append(dictionary)
    return result_list


test = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

print(filter_by_state(test))


def sort_by_date(dictionaries: list[dict], order: bool = True) -> list[dict]:
    """Функция, которая принимает список словарей и за счет необязательного параметра сортирует список по дате"""
    result = sorted(dictionaries, key=lambda x: x["date"], reverse=order)
    return result


test_sort_by_date = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

order = 'False'
print(sort_by_date(test_sort_by_date))
