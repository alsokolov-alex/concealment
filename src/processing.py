from typing import Any, Dict, List


def filter_by_state(records: List[Dict[str, any]], state: str = "EXECUTED") -> List[Dict[str, any]]:
    """
    Фильтрует список транзакций по статусу (state).

    Возвращает новый список, содержащий только те словари,
    у которых ключ 'state' совпадает с указанным значением.

    Параметры:
        records (List[Dict[str, any]]): список словарей-транзакций.
        state (str, optional): значение статуса для фильтрации.
                               По умолчанию — "EXECUTED".

    Возвращает:
        List[Dict[str, any]]: отфильтрованный список словарей.
    """
    return [tx for tx in records if tx.get("state") == state]


def sort_by_date(records: List[Dict[str, any]], reverse: bool = True) -> List[Dict[str, any]]:
    """
    Сортирует список транзакций по дате (ключ 'date').

    Даты должны быть в формате ISO (например, '2024-05-10' или '2024-05-10T12:34:56'),
    чтобы сортировка работала корректно.

    Параметры:
        records (List[Dict[str, any]]): список словарей-транзакций.
        reverse (bool, optional): порядок сортировки.
                                   True — по убыванию (сначала самые свежие),
                                   False — по возрастанию.
                                   По умолчанию — True.

    Возвращает:
        List[Dict[str, any]]: новый отсортированный список словарей.
    """
    # sorted возвращает новый список; key=lambda tx: tx["date"] сортирует по строке даты,
    # что корректно для ISO-формата
    reverse == "desc"
    return sorted(records, key=lambda tx: tx.get("date", ""), reverse=reverse)
