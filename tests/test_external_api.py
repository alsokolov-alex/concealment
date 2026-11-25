"""Тесты модуля external_api с использованием Mock и patch."""

import unittest
from unittest.mock import Mock, patch

from src.external_api import get_transaction_amount_in_rubles


class TestGetTransactionAmountInRubles(unittest.TestCase):
    """Тесты функции get_transaction_amount_in_rubles."""

    def setUp(self) -> None:
        self.rub_transaction = {
            "operationAmount": {
                "amount": "100.5",
                "currency": {"code": "RUB"},
            }
        }
        self.usd_transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"},
            }
        }
        self.eur_transaction = {
            "operationAmount": {
                "amount": "50",
                "currency": {"code": "EUR"},
            }
        }

        # Подменяем окружение на время всех тестов класса
        self.env_patcher = patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "test_key"})
        self.env_patcher.start()
        self.addCleanup(self.env_patcher.stop)

    def test_rub_returns_amount_without_api_call(self) -> None:
        """Для RUB сумма возвращается без обращения к API."""
        result = get_transaction_amount_in_rubles(self.rub_transaction)
        self.assertEqual(result, 100.5)

    @patch("src.external_api.requests.get")
    def test_usd_converts_via_api(self, mock_get: Mock) -> None:
        """Для USD происходит обращение к API и конвертация."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": 7500.0}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_transaction_amount_in_rubles(self.usd_transaction)
        self.assertEqual(result, 7500.0)
        mock_get.assert_called_once()

    @patch("src.external_api.requests.get")
    def test_eur_converts_via_api(self, mock_get: Mock) -> None:
        """Для EUR происходит обращение к API и конвертация."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": 5000.0}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_transaction_amount_in_rubles(self.eur_transaction)
        self.assertEqual(result, 5000.0)

    def test_unsupported_currency_raises(self) -> None:
        """Для неподдерживаемой валюты выбрасывается исключение."""
        transaction = {
            "operationAmount": {
                "amount": "10",
                "currency": {"code": "GBP"},
            }
        }
        with self.assertRaises(ValueError):
            get_transaction_amount_in_rubles(transaction)

    def test_missing_api_key_raises(self) -> None:
        """Если API-ключ не задан, выбрасывается исключение."""
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ValueError):
                get_transaction_amount_in_rubles(self.usd_transaction)
