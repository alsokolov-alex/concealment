import pytest

from src.processing import filter_by_state, sort_by_date
from typing import Any, Dict, List

@pytest.fixture
def test_filter_executed_only():
    records: List[Dict[str, Any]] = [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "state": "CANCELED", "amount": 200},
        {"id": 3, "state": "EXECUTED", "amount": 300},
    ]
    result = filter_by_state(records, "EXECUTED")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_default_state_is_executed():
    records: List[Dict[str, Any]] = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
    ]
    result = filter_by_state(records)
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_empty_list():
    records: List[Dict[str, Any]] = []
    result = filter_by_state(records, "EXECUTED")
    assert result == []


def test_missing_state_key_excluded():
    records: List[Dict[str, Any]] = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2},  # нет ключа state
        {"id": 3, "status": "EXECUTED"},  # другой ключ
    ]
    result = filter_by_state(records, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 1

def test_sort_by_date_desc():
    records: List[Dict[str, Any]] = [
        {"id": 1, "date": "2024-01-01"},
        {"id": 2, "date": "2024-03-01"},
        {"id": 3, "date": "2024-02-01"},
    ]
    result = sort_by_date(records, reverse=True)
    # по убыванию: 2024-03-01, 2024-02-01, 2024-01-01
    assert [tx["id"] for tx in result] == [2, 3, 1]


def test_sort_by_date_asc():
    records: List[Dict[str, Any]] = [
        {"id": 1, "date": "2024-01-01"},
        {"id": 2, "date": "2024-03-01"},
        {"id": 3, "date": "2024-02-01"},
    ]
    result = sort_by_date(records, reverse=False)
    # по возрастанию: 2024-01-01, 2024-02-01, 2024-03-01
    assert [tx["id"] for tx in result] == [1, 3, 2]


def test_default_reverse_is_true():
    records: List[Dict[str, Any]] = [
        {"id": 1, "date": "2024-01-01"},
        {"id": 2, "date": "2024-03-01"},
    ]
    # без указания reverse — по умолчанию True (убывание)
    result = sort_by_date(records)
    assert [tx["id"] for tx in result] == [2, 1]


def test_empty_list():
    records: List[Dict[str, Any]] = []
    result = sort_by_date(records)
    assert result == []


def test_missing_date_key():
    """
    Записи без 'date' получают пустую строку в качестве ключа,
    поэтому при reverse=True они окажутся в конце.
    """
    records: List[Dict[str, Any]] = [
        {"id": 1, "date": "2024-03-01"},
        {"id": 2},  # нет date
        {"id": 3, "date": "2024-01-01"},
    ]
    result = sort_by_date(records, reverse=True)
    # ожидаем: сначала даты по убыванию, потом без даты
    assert [tx["id"] for tx in result] == [1, 3, 2]


def test_iso_datetime_sorting():
    """
    ISO-строки сортируются лексикографически корректно.
    """
    records: List[Dict[str, Any]] = [
        {"id": 1, "date": "2024-05-10T10:00:00"},
        {"id": 2, "date": "2024-05-10T09:00:00"},
        {"id": 3, "date": "2024-05-09T23:59:59"},
    ]
    result = sort_by_date(records, reverse=True)
    # лексикографически: 10:00 > 09:00 > вчера
    assert [tx["id"] for tx in result] == [1, 2, 3]


def test_stable_sort():
    """
    sorted() в Python стабилен: записи с одинаковой датой сохраняют порядок.
    """
    records: List[Dict[str, Any]] = [
        {"id": 1, "date": "2024-01-01"},
        {"id": 2, "date": "2024-01-01"},
        {"id": 3, "date": "2024-01-01"},
    ]
    result = sort_by_date(records, reverse=True)
    assert [tx["id"] for tx in result] == [1, 2, 3]