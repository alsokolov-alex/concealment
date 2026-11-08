import functools
from datetime import datetime


def log(filename=None):
    """Декоратор для логирования выполнения функций.
    Логирует имя функции, результат выполнения или тип ошибки
    и входные параметры.

    Args:
        filename: путь к файлу лога. Если не задан — лог выводится в консоль.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                message = (
                    f"{func.__name__} error: {type(error).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )
                _write(message, filename)
                raise
            else:
                _write(f"{func.__name__} ok", filename)
                return result

        return wrapper

    return decorator


def _write(message: str, filename: str) -> None:
    if filename:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(message + "\n")
    else:
        print(message)