"""Тесты для декоратора log."""

from pathlib import Path
from typing import Any, Callable, Optional

import pytest

from src.decorators import log


def test_log_to_file_on_success(tmp_path: Path) -> None:
    """Успешное выполнение: в файл записывается 'ok'."""
    filename = tmp_path / "mylog.txt"

    @log(filename=str(filename))
    def add(x: int, y: int) -> int:
        return x + y

    assert add(1, 2) == 3
    assert filename.read_text(encoding="utf-8") == "add ok\n"


def test_log_to_console_on_success(capsys: pytest.CaptureFixture[str]) -> None:
    """Успешное выполнение: без filename лог выводится в консоль."""

    @log()
    def add(x: int, y: int) -> int:
        return x + y

    assert add(1, 2) == 3
    captured = capsys.readouterr()
    assert captured.out == "add ok\n"


def test_log_to_file_on_error(tmp_path: Path) -> None:
    """Ошибка: в файл пишутся тип ошибки и входные параметры."""
    filename = tmp_path / "mylog.txt"

    @log(filename=str(filename))
    def divide(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    content = filename.read_text(encoding="utf-8")
    assert content == "divide error: ZeroDivisionError. Inputs: (1, 0), {}\n"


def test_log_to_console_on_error(capsys: pytest.CaptureFixture[str]) -> None:
    """Ошибка без filename: сообщение уходит в консоль."""

    @log()
    def divide(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert captured.out == "divide error: ZeroDivisionError. Inputs: (1, 0), {}\n"


def test_log_error_with_kwargs(tmp_path: Path) -> None:
    """Ошибка при вызове с именованными аргументами: kwargs попадают в лог."""
    filename = tmp_path / "mylog.txt"

    @log(filename=str(filename))
    def divide(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(x=1, y=0)

    content = filename.read_text(encoding="utf-8")
    assert content == "divide error: ZeroDivisionError. Inputs: (), {'x': 1, 'y': 0}\n"


def test_log_preserves_function_name() -> None:
    """functools.wraps сохраняет имя и docstring исходной функции."""

    @log()
    def documented() -> None:
        """Docs."""

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "Docs."


def test_log_multiple_calls_append(tmp_path: Path) -> None:
    """Многократные вызовы дописывают строки в один файл."""
    filename = tmp_path / "mylog.txt"

    @log(filename=str(filename))
    def add(x: int, y: int) -> int:
        return x + y

    add(1, 2)
    add(3, 4)
    assert filename.read_text(encoding="utf-8") == "add ok\nadd ok\n"
