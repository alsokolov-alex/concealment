import builtins
import json
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from src.utils import get_transactions_from_csv, get_transactions_from_excel, get_transactions_from_json


class TestGetTransactionsFromJson:

    def test_reads_valid_file(self, sample_transactions: list[dict], tmp_path: Path) -> None:
        """Корректный файл возвращает список словарей."""
        file = tmp_path / "operations.json"
        file.write_text(json.dumps(sample_transactions), encoding="utf-8")

        result = get_transactions_from_json(str(file))

        assert result == sample_transactions

    def test_missing_file_returns_empty_list(self, tmp_path: Path) -> None:
        """Несуществующий файл возвращает пустой список."""
        assert get_transactions_from_json(str(tmp_path / "no_such.json")) == []

    def test_broken_json_returns_empty_list(self, tmp_path: Path) -> None:
        """Повреждённый JSON возвращает пустой список."""
        file = tmp_path / "broken.json"
        file.write_text("{не json", encoding="utf-8")

        assert get_transactions_from_json(str(file)) == []

    def test_json_not_list_returns_empty(self, tmp_path: Path) -> None:
        """JSON не со списком на верхнем уровне возвращает пустой список."""
        file = tmp_path / "not_list.json"
        file.write_text('{"key": "value"}', encoding="utf-8")

        assert get_transactions_from_json(str(file)) == []

    def test_mocked_open(self, mocker: MockerFixture, sample_transactions: list[dict]) -> None:
        """Чтение через мок open — файл не нужен на диске."""
        mock_file = mocker.mock_open(read_data=json.dumps(sample_transactions))
        mocker.patch.object(builtins, "open", mock_file)

        result = get_transactions_from_json("fake/path.json")

        assert result == sample_transactions


class TestGetTransactionsFromCsv:

    def test_reads_valid_file(self, sample_csv_content: str, tmp_path: Path) -> None:
        """Корректный CSV возвращает список словарей со строковыми значениями."""
        file = tmp_path / "operations.csv"
        file.write_text(sample_csv_content, encoding="utf-8")

        result = get_transactions_from_csv(str(file))

        assert len(result) == 2
        assert all(isinstance(row, dict) for row in result)
        assert result[0]["id"] == "650703.0"

    def test_missing_file_returns_empty_list(self, tmp_path: Path) -> None:
        """Несуществующий файл возвращает пустой список."""
        assert get_transactions_from_csv(str(tmp_path / "no_such.csv")) == []

    def test_empty_file(self, tmp_path: Path) -> None:
        """Пустой CSV возвращает пустой список."""
        file = tmp_path / "empty.csv"
        file.write_text("", encoding="utf-8")

        assert get_transactions_from_csv(str(file)) == []

    def test_mocked_open(self, mocker: MockerFixture, sample_csv_content: str) -> None:
        """Чтение через мок open."""
        mock_file = mocker.mock_open(read_data=sample_csv_content)
        mocker.patch.object(builtins, "open", mock_file)

        result = get_transactions_from_csv("fake/path.csv")

        assert len(result) == 2


class TestGetTransactionsFromExcel:

    def test_reads_real_file(self, tmp_path: Path) -> None:
        """Реальный XLSX-файл читается корректно."""
        data = {
            "id": [650703, 359721],
            "description": ["Перевод организации", "Перевод с карты на карту"],
        }
        file = tmp_path / "operations.xlsx"
        pd.DataFrame(data).to_excel(file, index=False)

        result = get_transactions_from_excel(str(file))

        assert len(result) == 2
        assert result[0]["id"] == 650703

    def test_missing_file_returns_empty_list(self, tmp_path: Path) -> None:
        """Несуществующий файл возвращает пустой список."""
        assert get_transactions_from_excel(str(tmp_path / "no_such.xlsx")) == []

    def test_mocked_read_excel(self, mocker: MockerFixture) -> None:
        """pandas.read_excel замокан — реальный файл не нужен."""
        mock_df = MagicMock()
        mock_df.fillna.return_value.to_dict.return_value = [
            {"id": 1, "description": "Перевод"},
        ]
        mocker.patch("src.utils.pd.read_excel", return_value=mock_df)

        result = get_transactions_from_excel("fake/path.xlsx")

        assert len(result) == 1
