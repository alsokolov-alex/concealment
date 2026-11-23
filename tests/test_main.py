import pytest
from pytest_mock import MockerFixture

from src.main import choice_of_file, main

sample_transactions: list[dict] = [
    {"id": 895315941, "state": "EXECUTED"},
    {"id": 869168149, "state": "CANCELED"},
]


class TestChoiceOfFile:
    """Тесты выбора функции чтения по расширению."""

    def test_json_extension(self, mocker: MockerFixture) -> None:
        """JSON-файл передаётся в get_transactions_from_json."""
        mock = mocker.patch("src.main.get_transactions_from_json", return_value=sample_transactions)

        result = choice_of_file("data/operations.json")

        mock.assert_called_once_with("data/operations.json")
        assert result == sample_transactions

    def test_csv_extension(self, mocker: MockerFixture) -> None:
        """CSV-файл передаётся в get_transactions_from_csv."""
        mock = mocker.patch("src.main.get_transactions_from_csv", return_value=[])

        assert choice_of_file("data/operations.csv") == []
        mock.assert_called_once()

    def test_xlsx_extension(self, mocker: MockerFixture) -> None:
        """XLSX-файл передаётся в get_transactions_from_excel."""
        mock = mocker.patch("src.main.get_transactions_from_excel", return_value=[])

        assert choice_of_file("data/operations.xlsx") == []
        mock.assert_called_once()

    def test_xls_extension(self, mocker: MockerFixture) -> None:
        """Старый формат .xls тоже поддержан."""
        mock = mocker.patch("src.main.get_transactions_from_excel", return_value=[])

        assert choice_of_file("data/operations.xls") == []
        mock.assert_called_once()

    def test_unknown_extension(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Неизвестное расширение возвращает пустой список и печатает сообщение."""
        result = choice_of_file("data/operations.txt")

        assert result == []
        assert "Неизвестный формат" in capsys.readouterr().out

    def test_uppercase_extension(self, mocker: MockerFixture) -> None:
        """Расширение регистронезависимо."""
        mock = mocker.patch("src.main.get_transactions_from_csv", return_value=[])
        choice_of_file("DATA/OPERATIONS.CSV")
        mock.assert_called_once()


class TestMain:
    """Тесты главной функции."""

    def test_main_prints_transactions(self, mocker: MockerFixture, capsys: pytest.CaptureFixture[str]) -> None:
        """main выводит каждую транзакцию в консоль."""
        mocker.patch("src.main.PATH_TO_FILE", "data/operations.json")
        mocker.patch("src.main.choice_of_file", return_value=sample_transactions)

        main()

        out = capsys.readouterr().out
        assert "895315941" in out
        assert "869168149" in out

    def test_main_with_empty_list(self, mocker: MockerFixture) -> None:
        """Пустой список — ошибок нет."""
        mocker.patch("src.main.choice_of_file", return_value=[])
        main()  # не должно упасть
