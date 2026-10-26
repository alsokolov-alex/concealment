import pytest

from src.processing import filter_by_state, sort_by_date

@pytest.fixture

def test_filter_by_state(lists, state, expected):
    assert filter_by_state(lists, state) == expected

@pytest.fixture

def test_sort_by_date(records, date, expected):
    assert sort_by_date(records, date) == expected
