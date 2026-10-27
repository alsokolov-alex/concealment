from typing import Any, Dict, List


data_list = dict[str, any]  # тип «запись» — словарь со строковыми ключами и любыми значениями


def filter_by_state(records: list[data_list], state: str = "EXECUTED") -> list[data_list]:
    """
    Фильтрует список транзакций по статусу (state).

    Возвращает новый список, содержащий только те словари,
    у которых ключ 'state' совпадает с указанным значением.

    Параметры:
        records (list[data_list]): список словарей-транзакций.
        state (str, optional): значение статуса для фильтрации.
                               По умолчанию — "EXECUTED".

    Возвращает:
        list[data_list]: отфильтрованный список словарей.
    """
    return [tx for tx in records if tx.get("state") == state]


def sort_by_date(records: list[data_list], reverse: bool = True) -> list[data_list]:
    """
    Сортирует список транзакций по дате (ключ 'date').

    Даты должны быть в формате ISO (например, '2024-05-10' или '2024-05-10T12:34:56'),
    чтобы сортировка работала корректно.

    Параметры:
        records (list[data_list]): список словарей-транзакций.
        reverse (bool, optional): порядок сортировки.
                                   True — по убыванию (сначала самые свежие),
                                   False — по возрастанию.
                                   По умолчанию — True.

    Возвращает:
        list[data_list]: новый отсортированный список словарей.
    """
    # sorted возвращает новый список; key=lambda tx: tx["date"] сортирует по строке даты,
    # что корректно для ISO-формата
    reverse == "desc"
    return sorted(records, key=lambda tx: tx.get("date", ""), reverse=reverse)
