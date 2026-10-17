from src.masks import get_mask_account, get_mask_card_number


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

    is_account = lower_text.startswith("счёт") or lower_text.startswith("счет") or lower_text.startswith("account")

    parts = account_card.split()
    if len(parts) < 2:
        return "Укажите тип и номер карты или счёта."

    number_candidate = parts[-1]
    if not number_candidate.isdigit():
        return "Некорректный номер карты или счёта."

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


def get_date(date_string: str) -> str:
    # Дата всегда в формате "2024-03-11T02:26:18.671407"
    # Берём части: год (0-3), месяц (5-6), день (8-9)
    year = date_string[0:4]
    month = date_string[5:7]
    day = date_string[8:10]

    return f"{day}.{month}.{year}"
