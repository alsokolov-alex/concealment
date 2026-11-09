from typing import Any, Dict, Iterable, Iterator, List

Transaction = Dict[str, Any]


def filter_by_currency(transactions: Iterable[Transaction], currency: str) -> Iterator[Transaction]:
    """
    Возвращает генератор, который поочерёдно выдаёт транзакции,
    где код валюты совпадает с заданной (например, 'USD').

    Поддерживает структуру:
        transaction['operationAmount']['currency']['code']

    :param transactions: список словарей-транзакций
    :param currency: строка с кодом валюты, например 'USD'
    :yield: словари-транзакции, подходящие по валюте
    """
    for transaction in transactions:
        # Безопасный доступ через .get, чтобы не упасть, если поля нет
        tx_currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")
        if tx_currency == currency:
            yield transaction


def transaction_descriptions(transactions: Iterable[Transaction]) -> Iterator[str]:
    """
    Генератор, который поочерёдно выдаёт описание каждой операции.

    :param transactions: список словарей-транзакций
    :yield: строки с описанием операции (поле 'description')
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    Номера генерируются как последовательные 16‑значные числа в диапазоне [start, end].
    start и end — целые числа от 1 до 9999_9999_9999_9999.

    :param start: начальное значение (число, не строка)
    :param end: конечное значение (число, не строка)
    :yield: строки вида '0000 0000 0000 0001'
    """
    if not (1 <= start <= end):
        raise ValueError("start и end должны быть положительными, start <= end")

    for num in range(start, end + 1):
        # Форматируем число как 16-значную строку с ведущими нулями
        num_str = f"{num:016d}"
        # Разбиваем на группы по 4 цифры через пробел
        card_number = f"{num_str[0:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
        yield card_number
