import re


def filter_by_currency(records: list[dict], currency_code: str = "RUB") -> list[dict]:
    """
    Возвращает только операции в заданной валюте.

    Понимает оба формата данных:
    - вложенный (JSON): operationAmount.currency.code
    - плоский (CSV/XLSX): currency_code

    :param records: список словарей с транзакциями
    :param currency_code: код валюты (по умолчанию 'RUB')
    :return: отфильтрованный список словарей
    """
    result = []
    for transaction in records:
        # Вложенный формат (JSON)
        currency = (
            transaction.get("operationAmount", {}).get("currency", {}).get("code", "")
        )
        # Плоский формат (CSV/XLSX)
        if not currency:
            currency = transaction.get("currency_code", "") or ""

        if currency.upper() == currency_code.upper():
            result.append(transaction)
    return result



def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Возвращает операции, в описании которых есть строка поиска.

    Использует re: поиск без учёта регистра, спецсимволы экранируются.

    :param data: список словарей с транзакциями
    :param search: строка для поиска в описании
    :return: список подходящих словарей
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result = []
    for transaction in data:
        description = transaction.get("description")
        if description and pattern.search(description):
            result.append(transaction)
    return result


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Считает количество операций в каждой категории (поиск по полю description).

    :param data: список словарей с транзакциями
    :param categories: список названий категорий
    :return: словарь {категория: количество операций}
    """
    counts = {}
    for category in categories:
        pattern = re.compile(re.escape(category), re.IGNORECASE)
        counts[category] = sum(
            1
            for transaction in data
            if transaction.get("description") and pattern.search(transaction["description"])
        )
    return counts

def filter_by_state(lists, state="EXECUTED"):
    """
    Возвращает новый список словарей, где значение ключа 'state' равно указанному.

    :param lists: список словарей (например, список транзакций/задач)
    :param state: строка со значением state (по умолчанию 'EXECUTED')
    :return: отфильтрованный список словарей
    """

    result = []
    for data_list in lists:
        # Проверяем, есть ли ключ 'state' и совпадает ли его значение с нужным
        if data_list.get("state") == state:
            result.append(data_list)
    return result


from datetime import datetime


def sort_by_date(records, descending=True):
    """
    Сортирует список словарей по полю 'date'.

    Параметры:
        records: список словарей, у каждого есть ключ 'date' со строкой в формате ISO
        descending: если True — сортировка по убыванию (сначала самые новые), иначе по возрастанию

    Возвращает:
        Новый отсортированный список (исходный не меняется).
    """

    def parse_date(item):
        raw = str(item.get("date", "")).strip()
        # берём только первые 19 символов "YYYY-MM-DD..."
        return raw[:19] if raw else ""

    return sorted(records, key=parse_date, reverse=descending)
