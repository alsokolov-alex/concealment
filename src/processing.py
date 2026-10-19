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
    Сортирует по полю 'date' в формате ISO (YYYY-MM-DD...).
    Если даты нет или она пустая, такие записи идут в конец при убывании,
    и в начало при возрастании.
    """

    def sort_key(r: Record) -> str:
        # Если даты нет или пустая — возвращаем пустую строку.
        # При descending=True пустые будут в конце, при False — в начале.
        return r.get("date", "") or ""

    return sorted(records, key=sort_key, reverse=descending)
