"""Модуль с функциями маскировки данных банковских карт и счетов."""

import logging
import os

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты: показывает первые 6 и последние 4 цифры.

    Args:
        card_number: Номер карты в виде строки из цифр.

    Returns:
        Строка замаскированного номера вида 'XXXX XX** **** XXXX'.

    Raises:
        ValueError: Если номер карты пуст или не состоит из цифр.
    """
    if not card_number or not card_number.isdigit():
        logger.error("Некорректный номер карты: %r", card_number)
        raise ValueError("Номер карты должен содержать только цифры")

    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    logger.info("Номер карты успешно замаскирован")
    return masked


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счёта: показывает только последние 4 цифры.

    Args:
        account_number: Номер счёта в виде строки из цифр.

    Returns:
        Строка замаскированного номера вида '**XXXX'.

    Raises:
        ValueError: Если номер счёта короче 4 цифр или не состоит из цифр.
    """
    if not account_number or not account_number.isdigit() or len(account_number) < 4:
        logger.error("Некорректный номер счёта: %r", account_number)
        raise ValueError("Номер счёта должен содержать минимум 4 цифры")

    masked = f"**{account_number[-4:]}"
    logger.info("Номер счёта успешно замаскирован")
    return masked
