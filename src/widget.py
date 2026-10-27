from typing import Any, Dict, List

from src.masks import get_mask_account, get_mask_card_number
from datetime import datetime

def mask_account_card(account_card: str) -> str:
    """
    Возвращаем строку с замаскированным номером.
    Для карт и счетов используются разные типы маскировки.
    """
    if not isinstance(account_card, str):
        return "Некорректный ввод: ожидается строка."

    account_card = account_card.strip()
    if not account_card:
        return "Укажите тип и номер карты или счёта."

    lower_text = account_card.lower()

    is_account = (
            "счёт" in lower_text or
            "счет" in lower_text or
            "account" in lower_text)
    is_card = "карта" in lower_text and not is_account

    parts = account_card.split()
    if len(parts) < 2:
        return "Укажите тип и номер карты или счёта."

    number_candidate = parts[-1]
    if not number_candidate.isdigit():
        return "Некорректный номер карты или счёта."

    try:
        if is_account:
            masked = get_mask_account(number_candidate)
            if masked is None:
                return "Некорректный номер счёта."
            prefix = " ".join(parts[:-1])
            return f"{prefix} {masked}"
        else:
            masked = get_mask_card_number(number_candidate)
            if masked is None:
                return "Некорректный номер карты."
            prefix = " ".join(parts[:-1])
            return f"{prefix} {masked}"
    except ValueError:
        # Ловим именно ту ошибку, которую ты видишь в тестах
        if is_account:
            return "Некорректный номер счёта."
        else:
            return "Некорректный номер карты."
    except Exception:
        # На всякий случай ловим всё остальное
        return "Произошла ошибка при маскировании номера."


def get_date(date_string: str) -> str:
    # Дата всегда в формате "2024-03-11T02:26:18.671407"
    # ValueError: если строка не соответствует ожидаемому формату.

    if not isinstance(date_string, str):
        raise ValueError("Ожидается строка.")

    try:
        dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError as e:
        raise ValueError(f"Неверный формат даты: {date_string}") from e

    return f"{dt.day:02d}.{dt.month:02d}.{dt.year}"
