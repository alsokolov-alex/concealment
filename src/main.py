from src.utils import get_transactions_from_csv, get_transactions_from_excel, get_transactions_from_json

PATH_TO_FILE = "data/transactions.csv"
PATH_TO_FILE = "data/operations.json"
PATH_TO_FILE = "data/transactions_excel.xlsx"


def choice_of_file(PATH_TO_FILE: str) -> list[dict]:
    """Выбирает функцию чтения в зависимости от расширения файла."""
    extension = PATH_TO_FILE.rsplit(".", 1)[-1].lower()

    if extension == "json":
        return get_transactions_from_json(PATH_TO_FILE)
    elif extension == "csv":
        return get_transactions_from_csv(PATH_TO_FILE)
    elif extension in ("xlsx", "xls"):
        return get_transactions_from_excel(PATH_TO_FILE)
    else:
        print("Неизвестный формат файла. Поддерживаются: json, csv, xlsx")
        return []


def main() -> None:
    transactions = choice_of_file(PATH_TO_FILE)

    for transaction in transactions:
        print(transaction)


if __name__ == "__main__":
    main()
