"""Модуль с утилитами для работы с файлами транзакций."""

import json
from typing import Any, List

file_path = "./data/operation.json"


def get_transactions_from_json(file_path: str) -> List[dict]:
    """Читает JSON-файл и возвращает список словарей с данными о финансовых транзакциях.

    Args:
        file_path: Путь до JSON-файла с транзакциями.

    Returns:
        Список словарей с данными о транзакциях.
        Пустой список, если файл не найден, пустой или содержит не список.
    """
    try:
        with open(file_path, encoding="utf-8") as file:
            data: Any = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if isinstance(data, list):
        return data
    return []
