import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


def test_filter_by_currency_returns_matching_transactions():
    transactions = [{"id": 1,
            "operationAmount": {"currency": {"code": "USD"}}},
                    {"id": 2,
            "operationAmount": {"currency": {"code": "EUR"}}},
                    {"id": 3,
            "operationAmount": {"currency": {"code": "USD"}}}]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_filter_by_currency_empty_result():
    transactions = [{"id": 1, "operationAmount": {"currency": {"code": "EUR"}}}]
    result = list(filter_by_currency(transactions, "USD"))
    assert result == []


def test_filter_by_currency_handles_missing_fields_safely():
    # Проверка, что отсутствие полей не ломает генератор
    transactions = [{},  # нет operationAmount
        {"operationAmount": {}},  # нет currency
        {"operationAmount": {"currency": {}}},  # нет code
        {"operationAmount": {"currency": {"code": "USD"}}}]
    result = list(filter_by_currency(transactions, "USD"))
    # Должна пройти только последняя транзакция
    assert len(result) == 1
    assert result[0] == transactions[-1]


def test_filter_by_currency_empty_list():
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_transaction_descriptions_returns_descriptions():
    transactions = [{"description": "Перевод организации"},
                    {"description": "Перевод со счета на счет"},
                    {"description": "Перевод с карты на карту"}]
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту"]


def test_transaction_descriptions_handles_missing_description():
    transactions = [{"description": "Есть описание"},
        {},  # нет description
        {"other_field": "что-то"}]
    descriptions = list(transaction_descriptions(transactions))
    # .get("description", "") вернёт пустую строку, если поля нет
    assert descriptions == ["Есть описание", "", ""]


def test_transaction_descriptions_empty_list():
    descriptions = list(transaction_descriptions([]))
    assert descriptions == []


def test_card_number_generator_basic_range():
    cards = list(card_number_generator(1, 5))
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005"]
    assert cards == expected


def test_card_number_generator_single_value():
    cards = list(card_number_generator(100, 100))
    assert cards == ["0000 0000 0000 0100"]


def test_card_number_generator_boundary_large_number():
    # Форматирование корректно и для больших чисел
    cards = list(card_number_generator(9999999999999998, 9999999999999999))
    assert cards == [
        "9999 9999 9999 9998",
        "9999 9999 9999 9999"]


def test_card_number_generator_invalid_range_raises():
    with pytest.raises(ValueError):
        list(card_number_generator(5, 1))  # start > end

    with pytest.raises(ValueError):
        list(card_number_generator(0, 5))  # start < 1


def test_functions_are_generators():
    assert hasattr(filter_by_currency([], "USD"), "__iter__")
    assert hasattr(transaction_descriptions([]), "__iter__")
    assert hasattr(card_number_generator(1, 2), "__iter__")