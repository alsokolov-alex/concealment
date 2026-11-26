from src.processing import (
    filter_by_currency,
    filter_by_state,
    process_bank_search,
    sort_by_date,
)
from src.utils import (
    get_transactions_from_csv,
    get_transactions_from_excel,
    get_transactions_from_json,
    mask_number,
)

FILES_BY_MENU = {
    "1": "data/operations.json",
    "2": "data/transactions.csv",
    "3": "data/transactions_excel.xlsx",
}

VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def choice_of_file(file_path: str) -> list[dict]:
    """Выбирает функцию чтения в зависимости от расширения файла."""
    extension = file_path.rsplit(".", 1)[-1].lower()

    if extension == "json":
        return get_transactions_from_json(file_path)
    elif extension == "csv":
        return get_transactions_from_csv(file_path)
    elif extension in ("xlsx", "xls"):
        return get_transactions_from_excel(file_path)
    else:
        print("Неизвестный формат файла. Поддерживаются: json, csv, xlsx")
        return []


def ask_yes_no(question: str) -> bool:
    """Задаёт вопрос Да/Нет и возвращает True/False."""
    answer = input(question + " ").strip().lower()
    return answer in ("да", "yes", "y", "д")


def ask_status() -> str:
    """Запрашивает статус, повторяя ввод до корректного значения."""
    while True:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        ).strip().upper()

        if status in VALID_STATUSES:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status

        print(f'Статус операции "{status}" недоступен.')


def format_transaction(transaction: dict) -> str:
    """Форматирует одну транзакцию для вывода в консоль."""
    date_raw = transaction.get("date", "")
    if date_raw and date_raw[4] == "-":
        year, month, day = date_raw[:10].split("-")
        date = f"{day}.{month}.{year}"
    else:
        date = date_raw[:10] if date_raw else "—"

    description = transaction.get("description", "Нет описания") or "Нет описания"

    nested = transaction.get("operationAmount") or {}
    amount = nested.get("amount", transaction.get("amount", "0"))
    currency = nested.get("currency", {})
    code = currency.get("code", transaction.get("currency_code", ""))
    if isinstance(amount, float) and amount == int(amount):
        amount = int(amount)
    currency_out = "руб." if str(code).upper() == "RUB" else code

    # Новое: маскируем номера карт и счетов перед выводом
    from_info = mask_number(transaction.get("from") or "")
    to_info = mask_number(transaction.get("to") or "")
    3
    # Стрелка только если есть и отправитель, и получатель
    if from_info and to_info:
        route = f"{from_info} -> {to_info}"
    else:
        route = from_info or to_info

    lines = [f"{date} {description}"]
    if route:
        lines.append(route)
    lines.append(f"Сумма: {amount} {currency_out}")
    return "\n".join(lines)


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input().strip()

    if choice not in FILES_BY_MENU:
        print("Некорректный пункт меню. Программа завершена.")
        return

    file_path = FILES_BY_MENU[choice]
    print(f"Для обработки выбран файл: {file_path}")

    transactions = choice_of_file(file_path)
    if not transactions:
        print("Не удалось загрузить транзакции из файла.")
        return

    status = ask_status()
    result = filter_by_state(transactions, status)

    if ask_yes_no("Отсортировать операции по дате? Да/Нет"):
        direction = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        # Ваша sort_by_date по умолчанию сортирует по убыванию (descending=True)
        descending = "возраст" not in direction
        result = sort_by_date(result, descending=descending)

    if ask_yes_no("Выводить только рублевые транзакции? Да/Нет"):
        result = filter_by_currency(result, "RUB")

    if ask_yes_no("Отфильтровать список транзакций по определенному слову в описании? Да/Нет"):
        search = input("Введите слово для поиска: ").strip()
        if search:
            result = process_bank_search(result, search)

    print("Распечатываю итоговый список транзакций...\n")

    if not result:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(result)}\n")
    for transaction in result:
        print(format_transaction(transaction))
        print()


if __name__ == "__main__":
    main()
