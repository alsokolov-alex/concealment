from src.utils import get_transactions_from_csv, get_transactions_from_excel, get_transactions_from_json

file_path = "data/transactions.csv"
file_path = "data/operations.json"
file_path = "data/transactions_excel.xlsx"


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


def main() -> None:
    transactions = choice_of_file(file_path)

    for transaction in transactions:
        print(transaction)


if __name__ == "__main__":
    main()
