"""Тесты модуля utils."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

from src.utils import get_transactions_from_json


class TestGetTransactionsFromJson(unittest.TestCase):
    """Тесты функции get_transactions_from_json."""

    def test_returns_list_of_transactions(self) -> None:
        """Возвращает список словарей из корректного файла."""
        data = [{"id": 1, "amount": 100.0}]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(data, f)
            path = f.name
        try:
            result = get_transactions_from_json(path)
            self.assertEqual(result, data)
        finally:
            os.remove(path)

    def test_file_not_found_returns_empty_list(self) -> None:
        """Если файл не найден — возвращается пустой список."""
        result = get_transactions_from_json("no_such_file.json")
        self.assertEqual(result, [])

    def test_invalid_json_returns_empty_list(self) -> None:
        """Если JSON некорректен — возвращается пустой список."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
            f.write("{not valid json")
            path = f.name
        try:
            result = get_transactions_from_json(path)
            self.assertEqual(result, [])
        finally:
            os.remove(path)

    def test_not_a_list_returns_empty_list(self) -> None:
        """Если файл содержит не список — возвращается пустой список."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump({"key": "value"}, f)
            path = f.name
        try:
            result = get_transactions_from_json(path)
            self.assertEqual(result, [])
        finally:
            os.remove(path)

    @patch("builtins.open")
    def test_open_called_with_mock(self, mock_open: unittest.mock.Mock) -> None:
        """Чтение файла перехватывается через patch (Mock)."""
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps([{"id": 1}])
        result = get_transactions_from_json("fake_path.json")
        self.assertEqual(result, [{"id": 1}])
        mock_open.assert_called_once_with("fake_path.json", encoding="utf-8")
