"""Модуль с утилитами для работы с файлами транзакций."""

import csv
import json
import logging
import os
import re
from typing import Any

import pandas as pd

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    os.makedirs("logs", exist_ok=True)
    file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def get_transactions_from_json(file_path: str) -> list[dict]:
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
    transactions: list[dict] = []
    try:
        with open(file_path, encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                transactions.append({key: (value or "") for key, value in row.items()})
    except FileNotFoundError:
        logger.error("Файл не найден: %s", file_path)
    except Exception:
        logger.exception("Ошибка чтения CSV-файла: %s", file_path)
    return transactions


def get_transactions_from_excel(file_path: str) -> list[dict]:
    """Считывает финансовые операции из XLSX-файла и возвращает список словарей."""
    try:
        df = pd.read_excel(file_path)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
        for column in df.columns:
            if column in ("amount", "operationAmount"):
                continue
            if df[column].dtype == "float64":
                df[column] = df[column].apply(
                    lambda value: str(int(value)) if value == value and value == int(value) else str(value)
                )
        transactions = df.fillna("").to_dict(orient="records")
    except FileNotFoundError:
        logger.error("Файл не найден: %s", file_path)
        transactions = []
    except (ValueError, KeyError):
        # ValueError — испорченный xlsx, KeyError — сбойный xml внутри книги
        logger.error("Не удалось прочитать XLSX-файл: %s", file_path)
        transactions = []
    return transactions


def mask_number(value: str) -> str:
    """Маскирует номер карты или счёта в строке.

    'Visa 0773092093872450'     -> 'Visa 0773 09** **** 2450'
    'Discover 8602781449570491' -> 'Discover 8602 78** **** 0491'
    'Счет 41878599375303475996' -> 'Счет **5996'

    Args:
        value: Строка с названием карты/счёта и номером.

    Returns:
        Строка с маскированным номером. Для пустой строки — пустая строка.
    """
    if not value:
        return ""

    digits = re.sub(r"\D", "", value)
    if not digits:
        return value
    # Счёт: показываем только последние 4 цифры
    if value.lower().startswith(("счет", "счёт", "account")):
        return f"Счет **{digits[-4:]}"
    # Карта: первые 6 и последние 4 цифры
    parts = value.rsplit(" ", 1)
    name = parts[0] if len(parts) == 2 and not parts[0][-1].isdigit() else ""
    if len(digits) < 16:
        return f"Счет **{digits[-4:]}"
    return f"{name} {digits[:4]} {digits[4:6]}** **** {digits[-4:]}".strip()
