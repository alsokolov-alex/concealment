from typing import Any, Dict, List

Record = Dict[str, Any]  # тип «запись» — словарь со строковыми ключами и любыми значениями


def filter_by_state(records: List[Record], state: str = "EXECUTED") -> List[Record]:
    """
    Возвращает новый список словарей, где значение ключа 'state' равно указанному.

    :param records: список словарей (например, список транзакций/задач)
    :param state: строка со значением state (по умолчанию 'EXECUTED')
    :return: отфильтрованный список словарей
    """
    result = []

    for record in records:

        if record.get("state") == state:
            result.append(record)
    return result


def sort_by_date(records: List[Record], descending: bool = True) -> List[Record]:
    """
    Возвращает новый список, отсортированный по полю 'date'.

    :param records: список словарей с ключом 'date'
    :param descending: если True — сортировка по убыванию (сначала свежие),
     если False — по возрастанию (сначала старые)
    :return: новый отсортированный список
    """

    return sorted(records, key=lambda r: r.get("date", ""), reverse=descending)
