"""Модуль с утилитами для работы с файлами транзакций."""

import json
import logging
import os
from typing import Any, List

file_path = "./data/operations.json"

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_transactions_from_json(file_path: str) -> List[dict]:
    """Читает JSON-файл и возвращает список словарей с данными о финансовых транзакциях.

    Args:
        file_path: Путь до JSON-файла с транзакциями.

    Returns:
        Список словарей с данными о транзакциях.
        Пустой список, если файл не найден, пустой или содержит не список.
    """
    logger.debug("Попытка чтения файла: %s", file_path)
    try:
        with open(file_path, encoding="utf-8") as file:
            data: Any = json.load(file)
    except FileNotFoundError:
        logger.error("Файл не найден: %s", file_path)
        return []
    except json.JSONDecodeError:
        logger.error("Некорректный JSON в файле: %s", file_path)
        return []

    if isinstance(data, list):
        logger.info("Прочитано %d транзакций из файла %s", len(data), file_path)
        return data

    logger.error("Содержимое файла %s не является списком", file_path)
    return []
