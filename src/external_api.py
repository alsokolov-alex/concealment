"""Модуль для конвертации валют через внешний API."""

import os
from typing import Any, Dict

import requests

API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def get_transaction_amount_in_rubles(transaction: Dict[str, Any]) -> float:
    """Возвращает сумму транзакции (amount) в рублях.

    Если валюта транзакции — RUB, сумма возвращается без конвертации.
    Если валюта — USD или EUR, происходит обращение к внешнему API
    Exchange Rates Data для получения курса и конвертации суммы.

    Args:
        transaction: Словарь с данными о транзакции.

    Returns:
        Сумма транзакции в рублях (float).

    Raises:
        ValueError: Если валюта транзакции не поддерживается.
        KeyError: Если в транзакции отсутствуют необходимые ключи.
    """
    currency_code: str = transaction["operationAmount"]["currency"]["code"]
    amount: float = float(transaction["operationAmount"]["amount"])

    if currency_code == "RUB":
        return amount

    if currency_code not in ("USD", "EUR"):
        raise ValueError(f"Неподдерживаемая валюта: {currency_code}")

    api_key = os.getenv("EXCHANGE_RATES_API_KEY")
    if not api_key:
        raise ValueError("Отсутствует API-ключ. Проверьте файл .env")

    response = requests.get(
        API_URL,
        params={"to": "RUB", "from": currency_code, "amount": str(amount)},
        headers={"apikey": api_key},
        timeout=10,
    )
    response.raise_for_status()
    result: float = float(response.json()["result"])
    return result
