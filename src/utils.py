"""Модуль с утилитами для работы с файлами транзакций."""

import csv
import json
import logging
import os
from typing import Any, List

import pandas as pd

PATH_TO_FILE = "./data/operations.json"
PATH_TO_FILE = "./data/transactions.csv"
PATH_TO_FILE = "./data/transactions_excel.xlsx"


logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_transactions_from_json(PATH_TO_FILE: str) -> List[dict]:
    """Читает JSON-файл и возвращает список словарей с данными о финансовых транзакциях.

    Args:
        file_path: Путь до JSON-файла с транзакциями.

    Returns:
        Список словарей с данными о транзакциях.
        Пустой список, если файл не найден, пустой или содержит не список.
    """
    logger.debug("Попытка чтения файла: %s", PATH_TO_FILE)
    try:
        with open(PATH_TO_FILE, encoding="utf-8") as file:
            data: Any = json.load(file)
    except FileNotFoundError:
        logger.error("Файл не найден: %s", PATH_TO_FILE)
        return []
    except json.JSONDecodeError:
        logger.error("Некорректный JSON в файле: %s", PATH_TO_FILE)
        return []

    if isinstance(data, list):
        logger.info("Прочитано %d транзакций из файла %s", len(data), PATH_TO_FILE)
        return data

    logger.error("Содержимое файла %s не является списком", PATH_TO_FILE)
    return []


def get_transactions_from_csv(PATH_TO_FILE: str) -> list[dict]:
    """Считывает финансовые операции из CSV-файла и возвращает список словарей."""
    transactions = []
    try:
        with open(PATH_TO_FILE, encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                transactions.append(dict(row))
    except FileNotFoundError:
        print(f"Файл {PATH_TO_FILE} не найден")
    return transactions


def get_transactions_from_excel(PATH_TO_FILE: str) -> list[dict]:
    """Считывает финансовые операции из XLSX-файла и возвращает список словарей."""
    try:
        df = pd.read_excel(PATH_TO_FILE)
        transactions = df.fillna("").to_dict(orient="records")
    except FileNotFoundError:
        print(f"Файл {PATH_TO_FILE} не найден")
        transactions = []
    return transactions
