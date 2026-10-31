from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

Transaction = Dict[str, Any]


def test_filter_by_currency_returns_matching_transactions() -> None:
    transactions: List[Transaction] = [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}},
        {"id": 3, "operationAmount": {"currency": {"code": "USD"}}},
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_filter_by_currency_empty_result() -> None:
    transactions: List[Transaction] = [{"id": 1, "operationAmount": {"currency": {"code": "EUR"}}}]
    result = list(filter_by_currency(transactions, "USD"))
    assert result == []


def test_filter_by_currency_handles_missing_fields_safely() -> None:
    transactions: List[Transaction] = [
        {},
        {"operationAmount": {}},
        {"operationAmount": {"currency": {}}},
        {"operationAmount": {"currency": {"code": "USD"}}},
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 1
    assert result[0] == transactions[-1]


def test_filter_by_currency_empty_list() -> None:
    # Для пустого списка mypy и так поймёт тип по контексту, но можно и так:
    transactions: List[Transaction] = []
    result = list(filter_by_currency(transactions, "USD"))
    assert result == []


def test_transaction_descriptions_returns_descriptions() -> None:
    transactions: List[Transaction] = [
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на карту"},
    ]
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту"]


def test_transaction_descriptions_handles_missing_description() -> None:
    transactions: List[Transaction] = [{"description": "Есть описание"}, {}, {"other_field": "что-то"}]
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == ["Есть описание", "", ""]


def test_transaction_descriptions_empty_list() -> None:
    transactions: List[Transaction] = []
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == []


def test_card_number_generator_basic_range() -> None:
    cards = list(card_number_generator(1, 5))
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]
    assert cards == expected


def test_card_number_generator_single_value() -> None:
    cards = list(card_number_generator(100, 100))
    assert cards == ["0000 0000 0000 0100"]


def test_card_number_generator_boundary_large_number() -> None:
    cards = list(card_number_generator(9999999999999998, 9999999999999999))
    assert cards == ["9999 9999 9999 9998", "9999 9999 9999 9999"]


def test_card_number_generator_invalid_range_raises() -> None:
    with pytest.raises(ValueError):
        list(card_number_generator(5, 1))

    with pytest.raises(ValueError):
        list(card_number_generator(0, 5))


def test_functions_are_generators() -> None:
    transactions: List[Transaction] = []
    assert hasattr(filter_by_currency(transactions, "USD"), "__iter__")
    assert hasattr(transaction_descriptions(transactions), "__iter__")
    assert hasattr(card_number_generator(1, 2), "__iter__")
