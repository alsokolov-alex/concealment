"""Модуль с утилитами для работы с файлами транзакций."""

import csv
import json
import logging
import os
from typing import Any, List

import pandas as pd

file_path = "./data/operations.json"
file_path = "./data/transactions.csv"
file_path = "./data/transactions_excel.xlsx"


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


def get_transactions_from_csv(file_path: str) -> list[dict]:
    """Считывает финансовые операции из CSV-файла и возвращает список словарей."""
    transactions = []
    try:
        with open(file_path, encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                transactions.append(dict(row))
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
    return transactions


def get_transactions_from_excel(file_path: str) -> list[dict]:
    """Считывает финансовые операции из XLSX-файла и возвращает список словарей."""
    try:
        df = pd.read_excel(file_path)
        transactions = df.fillna("").to_dict(orient="records")
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
        transactions = []
    return transactions
