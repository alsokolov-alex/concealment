def get_mask_card_number(card_number: str) -> str:
    """Работаем со строкой, оформляем 16 цифр для работы"""

    card_number = str(card_number)

    card_number = card_number.replace(" ", "").replace("-", "")

    if len(card_number) != 16:
        raise ValueError

    first_part = card_number[:6]

    last_part = card_number[-4:]

    middle_part = card_number[6:-4]

    masked_middle = "*" * len(middle_part)

    raw_masked = first_part + masked_middle + last_part

    blocks = []
    for i in range(0, len(raw_masked), 4):
        block = raw_masked[i : i + 4]
        blocks.append(block)

    result = " ".join(blocks)
    return result


def get_mask_account(account_number: str) -> str:
    """Работаем со строкой,собираем звёздочки + последние 4 цифры"""

    account_number = str(account_number)

    account_number = account_number.replace(" ", "").replace("-", "")

    if len(account_number) < 4:
        raise ValueError

    last_four = account_number[-4:]

    masked_account = "**" + last_four

    return masked_account
