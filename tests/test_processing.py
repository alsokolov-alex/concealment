import pytest

from src.processing import filter_by_state, sort_by_date

def test_filter_by_state(lists, state, expected):
    assert filter_by_state(lists, state) == expected

def test_sort_by_date(records, date, expected):
    assert sort_by_date(records, date) == expected
