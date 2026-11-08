import functools
from datetime import datetime
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Декоратор для логирования выполнения функций.
    Логирует имя функции, результат выполнения или тип ошибки
    и входные параметры.

    Args:
        filename: путь к файлу лога. Если не задан — лог выводится в консоль.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                message = f"{func.__name__} error: {type(error).__name__}. " f"Inputs: {args}, {kwargs}"
                _write(message, filename)
                raise
            else:
                _write(f"{func.__name__} ok", filename)
                return result

        return wrapper

    return decorator


def _write(message: str, filename: Optional[str]) -> None:
    if filename:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(message + "\n")
    else:
        print(message)
